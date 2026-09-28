from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.schema.payment import PaymentCreate, PaymentResponse, PaymentUpdate
from app.services import payment_service

router = APIRouter()


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: Annotated[int, Path(..., ge=1)], db: Annotated[Session, Depends(get_db)]
):
    payment = payment_service.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found"
        )
    return payment


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate, db: Annotated[Session, Depends(get_db)]):
    payment = payment_service.create_payment(db, payload)
    return payment


@router.patch("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: Annotated[int, Path(..., ge=1)],
    payload: PaymentUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    payment = payment_service.update_payment(db, payment_id, payload)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found"
        )
    return payment
