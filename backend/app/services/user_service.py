from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.exceptions import DomainException
from app.models import User

from firebase_admin import auth


def find_user(db: Session, uid: str):
    if not uid:
        raise DomainException("Invalid credentials.")
    existing_user = db.scalars(select(User).where(User.firebase_uid == uid)).first()
    if not existing_user:
        try:
            new_user_info = auth.get_user(uid)
            new_user_obj = {
                "firebase_uid": uid,
                "first_name": new_user_info.display_name,
                "last_name": new_user_info.display_name,
                "email": new_user_info.email
            }
            new_user = User(**new_user_obj)
            db.add(new_user)
            try:
                db.commit()
                db.refresh(new_user)
                return new_user
            except IntegrityError as e:
                db.rollback()
                raise DomainException(f"Failed to create user: {e!s}")
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occured while getting credentials.")
    return existing_user
