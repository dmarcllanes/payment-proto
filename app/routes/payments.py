import uuid

from fasthtml.common import Button, Div, H2, P, Span, Script, NotStr
from starlette.requests import Request

from app.database import execute
from app.models import ChargeRequest
from app.services import risk, xendit


def register(rt):
    @rt("/api/v1/payments/charge", methods=["POST"])
    async def charge(request: Request):
        form = await request.form()
        token_id = form.get("token_id", "")
        amount = float(form.get("amount", 0))
        currency = form.get("currency", "PHP")
        merchant_id = form.get("merchant_id", "demo_merchant")
        ip = request.client.host if request.client else "unknown"
        external_id = f"order_{uuid.uuid4().hex[:12]}"

        decision = await risk.evaluate(merchant_id, ip, amount)
        if not decision.allowed:
            await _log(merchant_id, amount, currency, ip, "risk_blocked", failure_code=decision.reason)
            return _error_card(f"Payment blocked: {decision.reason}")

        req = ChargeRequest(
            token_id=token_id,
            amount=amount,
            currency=currency,
            merchant_id=merchant_id,
            external_id=external_id,
        )

        try:
            result = await xendit.charge_card(req, card_last4="????")
            status = "succeeded" if result.status == "CAPTURED" else "failed"
            await _log(merchant_id, amount, currency, ip, status, xendit_charge_id=result.charge_id)
            return _success_overlay(result.charge_id, amount, currency)
        except xendit.XenditError as exc:
            await _log(merchant_id, amount, currency, ip, "failed", failure_code=exc.code)
            return _error_card(f"{exc.code}: {exc.message}")


def _success_overlay(charge_id: str, amount: float, currency: str):
    formatted = f"{currency} {amount:,.2f}"
    return Div(
        # Burst rings
        Div(cls="burst-ring"),
        Div(cls="burst-ring burst-ring-2"),
        # Content
        Div(
            # Animated SVG checkmark
            Div(
                NotStr('''<svg viewBox="0 0 52 52" width="44" height="44" fill="none"
                    stroke="white" stroke-width="5"
                    stroke-linecap="round" stroke-linejoin="round">
                  <polyline class="check-path" points="12,28 22,38 40,16"/>
                </svg>'''),
                cls="check-circle",
            ),
            H2("Payment Successful!", style="font-size:1.5rem;font-weight:800;color:#ffffff;margin-bottom:0.4rem;"),
            Div(formatted, style="font-size:2.4rem;font-weight:900;color:#00BFA5;margin-bottom:0.4rem;letter-spacing:-0.02em;"),
            P(f"Charge ID: {charge_id}", style="font-size:0.72rem;color:#64748b;margin-bottom:1.75rem;font-family:monospace;"),
            Button("Done →", onclick="closeSuccess()", cls="dismiss-btn"),
            cls="success-content",
        ),
        cls="success-overlay",
        onclick="if(event.target===this)this.remove()",
    )


def _error_card(message: str):
    return Div(
        Span(message, style="color:#f87171;font-weight:600;"),
        cls="result-card result-error",
    )


async def _log(merchant_id, amount, currency, ip, status, xendit_charge_id=None, failure_code=None):
    await execute(
        """
        INSERT INTO payment_attempts
            (merchant_id, card_last4, amount, currency, status, xendit_charge_id, failure_code, ip_address)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        """,
        merchant_id, "????", amount, currency, status, xendit_charge_id, failure_code, ip,
    )
