from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import DomainException
from app.models import Payment
from app.schema.payment import PaymentCreate, PaymentUpdate


def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()


def create_payment(db: Session, data: PaymentCreate):
    new_payment = Payment(**data.model_dump())
    db.add(new_payment)

    try:
        db.commit()
        db.refresh(new_payment)
        return new_payment
    except IntegrityError as e:
        db.rollback()
        raise DomainException(f"Failed to create payment: {e!s}")


def update_payment(db: Session, payment_id: int, data: PaymentUpdate):
    existing_payment = get_payment(db, payment_id)

    if existing_payment is None:
        return None

    updates = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(existing_payment, key, value)
    try:
        db.commit()
        db.refresh(existing_payment)
        return existing_payment
    except IntegrityError as e:
        db.rollback()
        raise DomainException(f"Failed to update payment: {e!s}")
