from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    """
    Represents a transaction in the system.

    Attributes:
        transaction_id (int, optional): The unique identifier for the transaction.
        listing_id (int): The ID of the listing involved in the transaction.
        buyer_id (int): The ID of the buyer in the transaction.
        seller_id (int): The ID of the seller in the transaction.
        transaction_date (datetime): The date and time when the transaction occurred.
        transaction_type (str): The type of transaction ("auction" or "buy_now").
        amount (float): The amount of money involved in the transaction (excluding shipping).
        shipping_cost (float): The cost of shipping associated with the transaction.
        payment_method (str): The method used for payment (e.g., credit card, PayPal).
        payment_status (str): The current payment status ("pending", "completed", "failed", "refunded").
        created_at (datetime, optional): The timestamp when the transaction was created. Defaults to the current time if not provided.
        updated_at (datetime, optional): The timestamp when the transaction was last updated. Defaults to the current time if not provided.
    """
    def __init__(
            self,
            listing_id: int,
            buyer_id: int,
            seller_id: int,
            transaction_date: datetime,
            transaction_type: str, # "auction", "buy_now"
            amount: float,
            shipping_cost: float,
            payment_method: str,
            payment_status: str, # "pending", "completed", "failed", "refunded"
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            transaction_id: int | None = None
    ):
        self.VALID_TRANSACTION_TYPES = {"auction", "buy_now"}
        self.VALID_PAYMENT_STATUSES = {"pending", "completed", "failed", "refunded"}

        # Type checks

        # Value checks
        if transaction_type not in self.VALID_TRANSACTION_TYPES:
            raise ValueError(f"Listing type must be one of {self.VALID_TRANSACTION_TYPES}, got '{transaction_type}' instead")
        if payment_status not in self.VALID_PAYMENT_STATUSES:
            raise ValueError(f"Listing type must be one of {self.VALID_PAYMENT_STATUSES}, got '{payment_status}' instead")

        self.transaction_id = transaction_id
        self.listing_id = listing_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.transaction_date = transaction_date
        self.transaction_type = transaction_type
        self.amount = amount
        self.shipping_cost = shipping_cost
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        """Converts the transaction object to a dictionary representation."""
        return {
            "transaction_id": self.transaction_id,
            "listing_id": self.listing_id,
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "transaction_date": self.transaction_date,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "shipping_cost": self.shipping_cost,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
