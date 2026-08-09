from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from app.models import SubscriptionInterval, SubscriptionStatus
class SubscriptionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    notes: str | None = Field(default=None, max_length=255)
    amount: Decimal = Field(..., gt=0)
    billing_day: int = Field(..., ge=1, le=31)
    start_date: date
    interval: SubscriptionInterval = SubscriptionInterval.MONTHLY

class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    notes: str | None
    amount: Decimal
    billing_day: int
    start_date: date
    interval: SubscriptionInterval
    status: SubscriptionStatus