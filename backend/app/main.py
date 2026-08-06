from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .models import subscription
from .db.engine import get_db, engine
from .schema.subscription import SubscriptionCreate, SubscriptionResponse

subscription.Base.metadata.create_all(bind=engine) 

app = FastAPI(root_path="/api")

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

@app.get("/health/")
def health_check():
    return {"status": "ok"}

@app.get("/subscriptions/")
def list_subscriptions(db: Session = Depends(get_db)):
    subscriptions = db.query(subscription.Subscription).all()
    return subscriptions

@app.post("/subscriptions/", response_model=SubscriptionResponse)
def create_subscription(data: SubscriptionCreate, db: Session = Depends(get_db)):
    new_subscription = subscription.Subscription(name=data.name)
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription