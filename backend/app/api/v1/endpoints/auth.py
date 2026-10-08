from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.auth.dependencies import get_firebase_uid

from app.schema.user import UserResponse
from app.services import user_service

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_me(firebase_uid: Annotated[str, Depends(get_firebase_uid)], db: Annotated[Session, Depends(get_db)]):
    user = user_service.find_user(db, firebase_uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user