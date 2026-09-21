from fastapi import status
from fastapi.testclient import TestClient

from app.db.engine import SessionLocal
from app.main import app
from app.models import Payment, PaymentStatus, Subscription

client = TestClient(app)


def test_create_payment_success():
    subscription_payload = {
        "name": "Test Subscription",
        "amount": "249.99",
        "billing_day": 12,
        "start_date": "2026-09-19",
    }

    subscription_id = None
    payment_id = None
    try:
        response = client.post("/v1/subscriptions/", json=subscription_payload)
        assert response.status_code == status.HTTP_201_CREATED
        response_body = response.json()
        assert isinstance(response_body["id"], int)
        subscription_id = response_body["id"]

        payment_payload = {
            "subscription_id": subscription_id,
            "amount": "249.99",
            "paid_date": "2026-09-19",
        }

        try:
            payment_response = client.post("/v1/payments/", json=payment_payload)
            assert payment_response.status_code == status.HTTP_201_CREATED
            payment_response_body = payment_response.json()
            assert isinstance(payment_response_body["id"], int)
            payment_id = payment_response_body["id"]
            assert (
                payment_response_body["subscription_id"]
                == payment_payload["subscription_id"]
            )
            assert payment_response_body["amount"] == payment_payload["amount"]
            assert payment_response_body["paid_date"] == payment_payload["paid_date"]
            assert payment_response_body["status"] == PaymentStatus.PENDING.value
            assert payment_response_body["term_number"] is None
        finally:
            with SessionLocal() as db:
                if payment_id is not None:
                    payment = db.get(Payment, payment_id)
                    if payment is not None:
                        db.delete(payment)
                        db.commit()

    finally:
        with SessionLocal() as db:
            if subscription_id is not None:
                subscription = db.get(Subscription, subscription_id)
                if subscription is not None:
                    db.delete(subscription)
                    db.commit()
