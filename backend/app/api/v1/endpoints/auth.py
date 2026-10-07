from typing import Annotated

from fastapi import APIRouter, Depends
from app.auth.dependencies import get_firebase_uid

router = APIRouter()

@router.get("/me")
def get_me(firebase_uid: Annotated[str, Depends(get_firebase_uid)]):
    return {"firebase_uid": firebase_uid}