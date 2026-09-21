from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import DomainException
from app.models import Payment
from app.schema.payment import PaymentCreate


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
