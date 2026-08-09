from fastapi import APIRouter
from .v1.router import api_router as v1_router

api_router = APIRouter()

api_router.include_router(v1_router, prefix="/v1", tags=["V1 API"])

@api_router.get("/health/", tags=["Health Check"])
def health_check():
    return {"status": "ok"}


