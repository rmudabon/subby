from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Subscription
from app.schema.subscription import SubscriptionCreate, SubscriptionUpdate
from app.exceptions import DomainException


def get_paginated_subscriptions(db: Session, page: int = 1, size: int = 10):
    subscriptions = db.query(Subscription).offset((page - 1) * size).limit(size).all()
    total = db.query(Subscription).count()

    return (subscriptions, total)


def get_subscription(db: Session, subscription_id: int):
    subscription = (
        db.query(Subscription).filter(Subscription.id == subscription_id).first()
    )
    return subscription


def create_subscription(db: Session, data: SubscriptionCreate):
    new_subscription = Subscription(**data.model_dump())
    db.add(new_subscription)
    try:
        db.commit()
        db.refresh(new_subscription)
        return new_subscription
    except IntegrityError as e:
        db.rollback()
        raise DomainException(f"Failed to create subscription: {str(e)}")


def update_subscription(db: Session, subscription_id: int, data: SubscriptionUpdate):
    existing_subscription = get_subscription(db, subscription_id)

    if not existing_subscription:
        return None

    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(existing_subscription, field, value)

    try:
        db.commit()
        db.refresh(existing_subscription)
        return existing_subscription
    except IntegrityError as e:
        db.rollback()
        raise DomainException(f"Failed to update subscription: {str(e)}")


def delete_subscription(db: Session, subscription_id: int):
    existing_subscription = get_subscription(db, subscription_id)

    if not existing_subscription:
        return None

    db.delete(existing_subscription)

    try:
        db.commit()
        return True
    except IntegrityError as e:
        db.rollback()
        raise DomainException(f"Failed to delete subscription: {str(e)}")
