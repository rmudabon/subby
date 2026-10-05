from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import PaymentStatus

from .helpers import find_invalid_null_fields


class PaymentCreate(BaseModel):
    subscription_id: int = Field(..., ge=1)
    amount: Decimal = Field(..., gt=0, examples=[Decimal("9.99")])
    term_number: int | None = Field(default=None, ge=1)


# Payment instances are generated ahead of time during creation of a subscription/installment.
# Payments ideally should only be updated if it has been paid and when it was paid.
class PaymentUpdate(BaseModel):
    status: PaymentStatus | None = Field(default=None)
    paid_date: date | None = Field(default=None)

    @model_validator(mode="after")
    def reject_null_for_required_fields(self):
        nullable_fields = {"paid_date"}

        invalid_fields = find_invalid_null_fields(self, nullable_fields)
        if invalid_fields:
            field_names = ", ".join(sorted(invalid_fields))
            raise ValueError(f"{field_names} must not be null")

        return self


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subscription_id: int
    amount: Decimal
    status: PaymentStatus
    term_number: int | None
    paid_date: date | None
