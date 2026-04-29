import uuid
import httpx
from app.config import settings
from app.models import ChargeRequest, ChargeResponse

XENDIT_BASE = "https://api.xendit.co"


def _auth() -> tuple[str, str]:
    return (settings.xendit_secret_key, "")


async def charge_card(req: ChargeRequest, card_last4: str) -> ChargeResponse:
    if settings.simulate_2d:
        return ChargeResponse(
            charge_id=f"sim_2d_{uuid.uuid4().hex[:16]}",
            status="CAPTURED",
            amount=req.amount,
            currency=req.currency,
            masked_card=f"**** **** **** {card_last4}",
        )
    payload = {
        "token_id": req.token_id,
        "external_id": req.external_id,
        "amount": float(req.amount),
        "currency": req.currency,
        "is_3ds": True,
        "descriptor": req.description or req.merchant_id,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{XENDIT_BASE}/credit_card_charges",
            json=payload,
            auth=_auth(),
        )

    if resp.status_code not in (200, 201):
        data = resp.json()
        raise XenditError(data.get("error_code", "UNKNOWN"), data.get("message", ""))

    data = resp.json()
    return ChargeResponse(
        charge_id=data["id"],
        status=data["status"],
        amount=data["charge_amount"],
        currency=data.get("currency", req.currency),
        masked_card=f"**** **** **** {card_last4}",
    )


class XenditError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")
