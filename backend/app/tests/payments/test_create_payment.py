from fastapi import status
from fastapi.testclient import TestClient

from app.db.engine import SessionLocal
from app.main import app
from app.models import Payment, PaymentStatus

def test_create_payment_success():
    payload = {
        ""
    }