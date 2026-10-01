from fastapi import status
from fastapi.testclient import TestClient

from app.db.engine import SessionLocal
from app.main import app
from app.models import Subscription, PaymentStatus

client = TestClient(app)


def test_payment_missing_returns_404():
    response = client.get("/v1/payments/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Payment not found"}


def test_payment_existing_returns_200():
    payload = {
        "name": "Test Subscription",
        "amount": "249.99",
        "billing_day": 12,
        "start_date": "2026-09-19",
    }

    subscription_id = None
    payment_id = None

    try:
        subscription_response = client.post("/v1/subscriptions/", json=payload)
        assert subscription_response.status_code == status.HTTP_201_CREATED
        subscription_id = subscription_response.json()["id"]

        payment_payload = {
            "subscription_id": subscription_id,
            "amount": payload["amount"],
        }

        payment_response = client.post("/v1/payments/", json=payment_payload)
        assert payment_response.status_code == status.HTTP_201_CREATED
        payment_id = payment_response.json()["id"]

        payment_get_response = client.get(f"/v1/payments/{payment_id}")
        assert payment_get_response.status_code == status.HTTP_200_OK
        payment = payment_get_response.json()
        assert payment["id"] == payment_id
        assert payment["subscription_id"] == subscription_id
        assert payment["amount"] == payload["amount"]
        assert payment["status"] == PaymentStatus.PENDING.value
    finally:
        with SessionLocal() as db:
            if subscription_id is not None:
                subscription = db.get(Subscription, subscription_id)
                if subscription is not None:
                    db.delete(subscription)
                    db.commit()
