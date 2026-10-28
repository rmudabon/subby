from datetime import date
from decimal import Decimal

from fastapi import status
from fastapi.testclient import TestClient

from app.auth.dependencies import get_current_user
from app.db.engine import SessionLocal
from app.main import app
from app.models import Subscription, User
from app.tests.common import fake_user

client = TestClient(app)

DEFAULT_PAGE_NUMBER = 1
DEFAULT_PAGE_SIZE = 10


def test_subscription_missing_returns_401():
    response = client.get("/v1/subscriptions/999999")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not Authenticated"}


def test_subscription_existing_returns_200():
    user_id = None
    subscription_id = None
    try:
        with SessionLocal() as db:
            user = User(
                display_name="Test User",
                email="list-test-single@example.com",
                firebase_uid="list-test-user-single",
            )
            db.add(user)
            db.flush()  # user.id is now available

            subscription = Subscription(
                name="Test Subscription",
                amount=Decimal("249.99"),
                billing_day=12,
                start_date=date(2026, 9, 19),
                user_id=user.id,
            )
            db.add(subscription)
            db.commit()

            user_id = user.id
            subscription_id = subscription.id

        app.dependency_overrides[get_current_user] = lambda: fake_user(user_id)
        subscription_get_response = client.get(f"/v1/subscriptions/{subscription_id}")
        assert subscription_get_response.status_code == status.HTTP_200_OK
        subscription = subscription_get_response.json()
        assert subscription["id"] == subscription_id
    finally:
        with SessionLocal() as db:
            if subscription_id is not None:
                subscription = db.get(Subscription, subscription_id)
                if subscription is not None:
                    db.delete(subscription)
                    db.commit()
            if user_id is not None:
                user = db.get(User, user_id)
                if user is not None:
                    db.delete(user)
                    db.commit()
        app.dependency_overrides.pop(get_current_user, None)


def test_subscription_access_another_user_returns_404():
    user_ids = None
    subscription_id = None
    try:
        with SessionLocal() as db:
            user_one = User(
                display_name="Test User",
                email="list-test-single@example.com",
                firebase_uid="list-test-user-single",
            )
            user_two = User(
                display_name="Test User 2",
                email="list-test-two@example.com",
                firebase_uid="list-test-user-two",
            )
            users = [user_one, user_two]
            db.add_all(users)
            db.flush()  # user.id is now available

            subscription = Subscription(
                name="Test Subscription",
                amount=Decimal("249.99"),
                billing_day=12,
                start_date=date(2026, 9, 19),
                user_id=user_one.id,
            )
            db.add(subscription)
            db.flush()
            user_ids = [user.id for user in users]
            subscription_id = subscription.id
            db.commit()

        app.dependency_overrides[get_current_user] = lambda: fake_user(user_ids[1])
        subscription_get_response = client.get(f"/v1/subscriptions/{subscription_id}")
        assert subscription_get_response.status_code == status.HTTP_404_NOT_FOUND
        subscription = subscription_get_response.json()
        assert subscription["detail"] == "Subscription not found"
    finally:
        with SessionLocal() as db:
            if subscription_id is not None:
                subscription = db.get(Subscription, subscription_id)
                if subscription is not None:
                    db.delete(subscription)
                    db.commit()
            if user_ids is not None:
                for user_id in user_ids:
                    user = db.get(User, user_id)
                    if user is not None:
                        db.delete(user)
                        db.commit()
        app.dependency_overrides.pop(get_current_user, None)
