from pydantic import BaseModel

class SubscriptionBase(BaseModel):
    name: str

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionResponse(SubscriptionBase):
    id: int

    class Config:
        from_attributes = True