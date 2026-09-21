from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_negative_amount_reject():
    payload = {
        "name": "Test Subscription",
        "amount": -1.00,
        "notes": "Testing Added Sub",
        "billing_day": 1,
        "start_date": "2026-01-01",
        "interval": "monthly",
    }

    response = client.post("/v1/subscriptions/", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    errors = response.json()["detail"]
    assert any(error["loc"] == ["body", "amount"] for error in errors)
