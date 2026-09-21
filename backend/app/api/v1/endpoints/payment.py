from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.schema.payment import PaymentCreate, PaymentResponse
from app.services import payment_service

router = APIRouter()


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate, db: Annotated[Session, Depends(get_db)]):
    payment = payment_service.create_payment(db, payload)
    return payment
