import firebase_admin
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from firebase_admin import auth

from app.main import app

client = TestClient(app)


@pytest.fixture
def fake_firebase(monkeypatch):
    fake_app = object()

    monkeypatch.setattr(firebase_admin, "get_app", lambda: fake_app)
    monkeypatch.setattr(
        auth, "verify_id_token", lambda token, app: {"uid": "test-user-123"}
    )


@pytest.mark.usefixtures("fake_firebase")
def test_me_ok():
    response = client.get("/v1/auth/me", headers={"Authorization": "Bearer test-user"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"firebase_uid": "test-user-123"}


@pytest.mark.usefixtures("fake_firebase")
def test_me_401_no_header():
    response = client.get("/v1/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not Authenticated"}


def test_me_401_invalid_credentials(monkeypatch):
    def reject_token(token: str) -> str:
        raise auth.InvalidIdTokenError("Fake token")

    monkeypatch.setattr("app.auth.dependencies.verify_firebase_token", reject_token)
    response = client.get("/v1/auth/me", headers={"Authorization": "Bearer test-user"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials"}
