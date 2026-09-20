import pytest
from pydantic import ValidationError

from app.schema.subscription import SubscriptionCreate


def test_create_subscription_rejects_zero_amount():
    payload = {
        "name": "Test Subscription",
        "amount": 0.00,
        "billing_day": 12,
        "start_date": "2026-09-19",
    }

    with pytest.raises(ValidationError):
        SubscriptionCreate(**payload)


def test_create_subscription_rejects_negative_amount():
    payload = {
        "name": "Test Subscription",
        "amount": -10.00,
        "billing_day": 12,
        "start_date": "2026-09-19",
    }

    with pytest.raises(ValidationError):
        SubscriptionCreate(**payload)


@pytest.mark.parametrize("billing_day", [1, 15, 31])
def test_create_subscription_accepts_valid_billing_day(billing_day: int):
    payload = {
        "name": "Test Subscription",
        "amount": 10.00,
        "billing_day": billing_day,
        "start_date": "2026-09-19",
    }

    subscription = SubscriptionCreate(**payload)
    assert subscription.billing_day == billing_day
