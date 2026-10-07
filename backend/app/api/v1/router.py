from fastapi import APIRouter

from .endpoints.payment import router as payment_router
from .endpoints.subscription import router as subscription_router
from .endpoints.auth import router as auth_router

api_router = APIRouter()

api_router.include_router(
    subscription_router, prefix="/subscriptions", tags=["Subscriptions"]
)
api_router.include_router(payment_router, prefix="/payments", tags=["Payments"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
