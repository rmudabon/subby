from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from fastapi import status
from fastapi.testclient import TestClient

from app.auth.dependencies import get_current_user
from app.db.engine import SessionLocal
from app.main import app
from app.models import Subscription, User

DEFAULT_PAGE_NUMBER = 1
DEFAULT_PAGE_SIZE = 10


client = TestClient(app)


def fake_user(fake_id: int):
    return SimpleNamespace(id=fake_id)


def test_list_subscription_user_missing_returns_401():
    response = client.get("/v1/subscriptions/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not Authenticated"}


def test_list_subscription_existing_returns_200():
    user_id = None
    subscription_id = None
    try:
        with SessionLocal() as db:
            user = User(
                display_name="Test User",
                email="list-test@example.com",
                firebase_uid="list-test-user",
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
        subscription_get_response = client.get("/v1/subscriptions/")
        assert subscription_get_response.status_code == status.HTTP_200_OK
        subscription_list = subscription_get_response.json()
        assert subscription_list["page"] == DEFAULT_PAGE_NUMBER
        assert subscription_list["size"] == DEFAULT_PAGE_SIZE
        assert subscription_list["total"] == 1
        assert len(subscription_list["items"]) == 1
        assert subscription_list["items"][0]["id"] == subscription_id
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
