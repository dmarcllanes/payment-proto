from decimal import Decimal
from pydantic import BaseModel, Field


class ChargeRequest(BaseModel):
    token_id: str
    amount: Decimal = Field(gt=0, le=999_999.99)
    currency: str = "PHP"
    merchant_id: str
    external_id: str
    description: str | None = None


class ChargeResponse(BaseModel):
    charge_id: str
    status: str
    amount: Decimal
    currency: str
    masked_card: str


class RiskDecision(BaseModel):
    allowed: bool
    reason: str | None = None
