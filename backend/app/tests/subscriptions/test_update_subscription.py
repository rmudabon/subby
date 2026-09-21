from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_update_reject_null_amount():
    payload = {
        "amount": -1.00,
    }

    response = client.patch("/v1/subscriptions/1", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT