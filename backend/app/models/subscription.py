from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Numeric, CheckConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.engine import Base
from .enums import SubscriptionInterval, SubscriptionStatus

if TYPE_CHECKING:
    from .installment import Installment
    from .payment import Payment

class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    # Amount for every billing cycle
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    billing_day: Mapped[int] = mapped_column(CheckConstraint("billing_day >= 1 AND billing_day <= 31"), nullable=False)

    start_date: Mapped[date] = mapped_column()
    interval: Mapped[SubscriptionInterval] = mapped_column(
        Enum(SubscriptionInterval, native_enum=False), 
        default=SubscriptionInterval.MONTHLY, 
        nullable=False
        )
    status: Mapped[SubscriptionStatus] = mapped_column(
        Enum(SubscriptionStatus, native_enum=False), 
        default=SubscriptionStatus.ACTIVE, 
        nullable=False
        )

    # 1-1
    installment: Mapped[Optional["Installment"]] = relationship(back_populates="subscription", uselist=False, cascade="all, delete-orphan")

    # 1-N
    payments: Mapped[List["Payment"]] = relationship(back_populates="subscription", cascade="all, delete-orphan")
