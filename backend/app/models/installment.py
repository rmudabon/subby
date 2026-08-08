from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base

if TYPE_CHECKING:
    from .subscription import Subscription


class Installment(Base):
    __tablename__ = "installments"

    id: Mapped[int] = mapped_column(primary_key=True)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id", ondelete="CASCADE"), unique=True, nullable=False)
    total_terms: Mapped[int] = mapped_column()
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    subscription: Mapped["Subscription"] = relationship(back_populates="installment", uselist=False)