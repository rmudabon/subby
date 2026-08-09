from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import Annotated
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.schema.subscription import SubscriptionCreate, SubscriptionResponse
from app.schema.common import PaginatedResponse
from app.services import subscription_service

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[SubscriptionResponse])
def list_subscriptions(page: Annotated[int, Query(ge=1, description="Page number")] = 1, 
                       size: Annotated[int, Query(ge=1, le=50, description="Number of items per page")] = 10,
                       db: Session = Depends(get_db)):
    items, total = subscription_service.get_paginated_subscriptions(db, page, size)
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size
    )

@router.get("/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription(subscription_id: Annotated[int, Path(..., ge=1, description="Subscription ID")], db: Session = Depends(get_db)):
    subscription = subscription_service.get_subscription(db, subscription_id)
    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    return subscription

@router.post("/", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
def create_subscription(payload: SubscriptionCreate, db: Session = Depends(get_db)):
    subscription = subscription_service.create_subscription(db, payload)
    return subscription