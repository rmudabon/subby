from fastapi import status
from fastapi.testclient import TestClient

from app.db.engine import SessionLocal
from app.main import app
from app.models import Subscription, SubscriptionInterval, SubscriptionStatus

client = TestClient(app)


def test_create_subscription_success():
    payload = {
        "name": "Test Subscription",
        "amount": "249.99",
        "billing_day": 12,
        "start_date": "2026-09-19",
    }

    subscription_id = None
    try:
        response = client.post("/v1/subscriptions/", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        response_body = response.json()
        assert isinstance(response_body["id"], int)
        subscription_id = response_body["id"]
        assert response_body["name"] == payload["name"]
        assert response_body["amount"] == payload["amount"]
        assert response_body["billing_day"] == payload["billing_day"]
        assert response_body["interval"] == SubscriptionInterval.MONTHLY.value
        assert response_body["status"] == SubscriptionStatus.ACTIVE.value
    finally:
        with SessionLocal() as db:
            if subscription_id is not None:
                subscription = db.get(Subscription, subscription_id)
                if subscription is not None:
                    db.delete(subscription)
                    db.commit()
