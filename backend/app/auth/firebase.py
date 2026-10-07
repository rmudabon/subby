import firebase_admin
from firebase_admin import auth


def verify_firebase_token(token: str) -> str:
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app()

    claims = auth.verify_id_token(token, app=app)
    return claims["uid"]
