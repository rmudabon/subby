from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.engine import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)