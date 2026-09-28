from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_payment_missing_returns_404():
    response = client.get("/v1/payments/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Payment not found"}