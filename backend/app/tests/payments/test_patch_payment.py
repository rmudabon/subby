from fastapi import status
from fastapi.testclient import TestClient

from app.db.engine import SessionLocal
from app.main import app
from app.models import PaymentStatus, Subscription

client = TestClient(app)


def test_payment_update_missing_returns_404():
    dummy_payment_id = 99999
    patch_payload = {"status": PaymentStatus.PENDING.value}

    response = client.patch(f"/v1/payments/{dummy_payment_id}", json=patch_payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Payment not found"}


def test_payment_update_status_null_returns_422():
    dummy_payment_id = 99999
    patch_payload = {"status": None}

    response = client.patch(f"/v1/payments/{dummy_payment_id}", json=patch_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_payment_update_returns_paid():
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

        patch_payload = {"status": PaymentStatus.PAID.value}
        patch_response = client.patch(f"/v1/payments/{payment_id}", json=patch_payload)
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.json()["status"] == PaymentStatus.PAID.value

    finally:
        with SessionLocal() as db:
            if subscription_id is not None:
                subscription = db.get(Subscription, subscription_id)
                if subscription is not None:
                    db.delete(subscription)
                    db.commit()
