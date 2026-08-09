class DomainException(Exception):
    """Base exceptions"""
    pass

class SubscriptionNotFound(DomainException):
    def __init__(self, subscription_id: int):
        self.subscription_id = subscription_id
        super().__init__(f"Subscription {subscription_id} not found.")