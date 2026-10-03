from fastapi import status
from fastapi.testclient import TestClient

from app.db.engine import SessionLocal
from app.main import app
from app.models import Subscription, SubscriptionInterval, SubscriptionStatus

client = TestClient(app)


def test_subscription_missing_returns_404():
    response = client.get("/v1/subscriptions/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Subscription not found"}


def test_subscription_existing_returns_200():
    payload = {
        "name": "Test Subscription",
        "amount": "249.99",
        "billing_day": 12,
        "start_date": "2026-09-19",
    }

    subscription_id = None

    try:
        subscription_response = client.post("/v1/subscriptions/", json=payload)
        assert subscription_response.status_code == status.HTTP_201_CREATED
        subscription_id = subscription_response.json()["id"]

        subscription_get_response = client.get(f"/v1/subscriptions/{subscription_id}")
        assert subscription_get_response.status_code == status.HTTP_200_OK
        subscription = subscription_get_response.json()
        assert subscription["id"] == subscription_id
        assert subscription["amount"] == payload["amount"]
        assert subscription["billing_day"] == payload["billing_day"]
        assert subscription["status"] == SubscriptionStatus.ACTIVE.value
        assert subscription["interval"] == SubscriptionInterval.MONTHLY.value
    finally:
        with SessionLocal() as db:
            if subscription_id is not None:
                subscription = db.get(Subscription, subscription_id)
                if subscription is not None:
                    db.delete(subscription)
                    db.commit()
