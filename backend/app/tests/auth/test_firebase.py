import firebase_admin
from firebase_admin import auth

from app.auth.firebase import verify_firebase_token


def test_verify_firebase_token_returns_uid(monkeypatch):
    fake_app = object()

    monkeypatch.setattr(firebase_admin, "get_app", lambda: fake_app)
    monkeypatch.setattr(
        auth, "verify_id_token", lambda token, app: {"uid": "test-user-123"}
    )

    assert verify_firebase_token("fake-token") == "test-user-123"
