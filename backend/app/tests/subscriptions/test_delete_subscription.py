from fastapi import status
from fastapi.testclient import TestClient

from app.db.engine import SessionLocal
from app.main import app
from app.models import Subscription

client = TestClient(app)


def test_delete_404_if_not_found():
    response = client.delete("/v1/subscriptions/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Subscription not found"}


def test_delete_subscription_success():
    payload = {
        "name": "Test Subscription",
        "amount": 10.00,
        "notes": "Testing Added Sub",
        "billing_day": 1,
        "start_date": "2026-01-01",
        "interval": "monthly",
    }
    subscription_id = None
    try:
        subscription_create_request = client.post("/v1/subscriptions/", json=payload)
        assert subscription_create_request.status_code == status.HTTP_201_CREATED
        subscription = subscription_create_request.json()
        subscription_id = subscription["id"]

        delete_request = client.delete(f"/v1/subscriptions/{subscription_id}")
        assert delete_request.status_code == status.HTTP_204_NO_CONTENT
        assert delete_request.content == b""

        get_request = client.get(f"/v1/subscriptions/{subscription_id}")
        assert get_request.status_code == status.HTTP_404_NOT_FOUND
        assert get_request.json() == {"detail": "Subscription not found"}
    finally:
        with SessionLocal() as db:
            if subscription_id is not None:
                subscription = db.get(Subscription, subscription_id)
                if subscription is not None:
                    db.delete(subscription)
                    db.commit()
