from enum import StrEnum

class SubscriptionInterval(StrEnum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class SubscriptionStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class PaymentStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    SKIPPED = "skipped"