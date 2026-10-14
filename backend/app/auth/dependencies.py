from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth
from sqlalchemy.orm import Session

from app.auth.firebase import verify_firebase_token
from app.db.engine import get_db
from app.models import User
from app.services import user_service

bearer_schema = HTTPBearer(auto_error=False)


def get_firebase_uid(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_schema)],
) -> str:
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        return verify_firebase_token(credentials.credentials)
    except auth.InvalidIdTokenError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exception


def get_current_user(
    firebase_uid: Annotated[str, Depends(get_firebase_uid)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    user = user_service.find_user(db, firebase_uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
