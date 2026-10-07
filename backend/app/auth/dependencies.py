from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth

from app.auth.firebase import verify_firebase_token

bearer_schema = HTTPBearer(auto_error=False)


def get_firebase_uid(
        credentials: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(bearer_schema)
        ]
) -> str:
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        return verify_firebase_token(credentials.credentials)
    except auth.InvalidIdTokenError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        ) from exception