from fastapi import APIRouter
from .endpoints.subscription import router as subscription_router

api_router = APIRouter()

api_router.include_router(subscription_router, prefix="/subscriptions", tags=["Subscriptions"])

