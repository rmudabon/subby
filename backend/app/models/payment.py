from decimal import Decimal
from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Numeric, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums import PaymentStatus

from app.db.engine import Base

if TYPE_CHECKING:
    from .subscription import Subscription

class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        UniqueConstraint("subscription_id", "term_number", name="uq_subscription_term")
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, native_enum=False), 
        default=PaymentStatus.PENDING, 
        nullable=False
        )
    # Null for indefinite subscriptions
    term_number: Mapped[int] = mapped_column(default=None, nullable=True)
    paid_date: Mapped[Optional[date]] = mapped_column(default=None, nullable=True)

    subscription: Mapped["Subscription"] = relationship(back_populates="payments")