from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import PaymentStatus


class PaymentCreate(BaseModel):
    subscription_id: int = Field(..., ge=1)
    amount: Decimal = Field(..., gt=0, examples=[Decimal("9.99")])
    term_number: int | None = Field(default=None, ge=1)
    paid_date: date | None = Field(default=None)


# Payment instances are generated ahead of time during creation of a subscription/installment.
# Payments ideally should only be updated if it has been paid and when it was paid.
class PaymentUpdate(BaseModel):
    status: PaymentStatus | None = Field(default=None)
    paid_date: date | None = Field(default=None)

    @model_validator(mode="after")
    def reject_null_for_required_fields(self):
        nullable_fields = {"paid_date"}

        for field_name in self.model_fields_set - nullable_fields:
            if getattr(self, field_name) is None:
                raise ValueError(f"{field_name} must not be null")

        return self


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subscription_id: int
    amount: Decimal
    status: PaymentStatus
    term_number: int | None
    paid_date: date | None
