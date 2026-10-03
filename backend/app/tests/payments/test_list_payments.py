from fastapi import status
from fastapi.testclient import TestClient

from app.db.engine import SessionLocal
from app.main import app
from app.models import Subscription

client = TestClient(app)

DEFAULT_PAGE_NUMBER = 1
DEFAULT_PAGE_SIZE = 10


def test_list_payment_empty_default_returns_empty():
    response = client.get("/v1/payments/?subscription_id=9999999")
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["page"] == DEFAULT_PAGE_NUMBER
    assert body["size"] == DEFAULT_PAGE_SIZE
    assert body["total"] == 0
    assert body["items"] == []


def test_list_payment_existing_returns_correct_data():
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

        payment_list_response = client.get(f"/v1/payments/?subscription_id={subscription_id}")
        assert payment_list_response.status_code == status.HTTP_200_OK
        payments = payment_list_response.json()
        assert payments["page"] == DEFAULT_PAGE_NUMBER
        assert payments["size"] == DEFAULT_PAGE_SIZE
        assert payments["total"] >= 1
        assert any(payment["id"] == payment_id for payment in payments["items"])
    finally:
        with SessionLocal() as db:
            if subscription_id is not None:
                subscription = db.get(Subscription, subscription_id)
                if subscription is not None:
                    db.delete(subscription)
                    db.commit()
