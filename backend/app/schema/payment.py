from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import PaymentStatus


class PaymentCreate(BaseModel):
    subscription_id: int = Field(..., ge=1)
    amount: Decimal = Field(..., gt=0, examples=[Decimal("9.99")])
    term_number: int | None = Field(default=None, ge=1)
    paid_date: date | None = Field(default=None)


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subscription_id: int
    amount: Decimal
    status: PaymentStatus
    term_number: int | None
    paid_date: date | None
