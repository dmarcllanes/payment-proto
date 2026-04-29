from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config import settings
from app.database import execute


def register(rt):
    @rt("/webhooks/xendit", methods=["POST"])
    async def xendit_webhook(request: Request):
        token = request.headers.get("x-callback-token", "")
        if token != settings.xendit_webhook_token:
            return Response("Unauthorized", status_code=401)

        data = await request.json()
        charge_id = data.get("id")
        status = data.get("status")

        if charge_id and status in ("CAPTURED", "FAILED"):
            db_status = "succeeded" if status == "CAPTURED" else "failed"
            await execute(
                "UPDATE payment_attempts SET status = $1 WHERE xendit_charge_id = $2",
                db_status,
                charge_id,
            )

        return JSONResponse({"received": True})
