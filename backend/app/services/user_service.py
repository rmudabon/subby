from firebase_admin import auth
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import DomainException
from app.models import User


def find_user(db: Session, uid: str):
    if not uid:
        raise DomainException("Invalid credentials.")
    existing_user = db.scalars(select(User).where(User.firebase_uid == uid)).first()
    if not existing_user:
        try:
            new_user_info = auth.get_user(uid)
        except auth.UserNotFoundError:
            return None
        email = new_user_info.email
        if not email:
            raise DomainException("Firebase account has no email.")

        display_name = (
            new_user_info.display_name or email.split("@", maxsplit=1)[0] or "New User"
        )
        new_user = User(firebase_uid=uid, email=email, display_name=display_name)
        db.add(new_user)
        try:
            db.commit()
            db.refresh(new_user)
            return new_user
        except IntegrityError as e:
            db.rollback()
            raise DomainException(f"Failed to create user: {e!s}") from e

    return existing_user
