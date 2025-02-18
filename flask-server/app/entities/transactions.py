from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    """
    Represents a transaction in the system.

    Attributes:
        transaction_id (int, optional): The unique identifier for the transaction.
        listing_id (int): The ID of the listing involved.
        buyer_id (int): The ID of the buyer.
        seller_id (int): The ID of the seller.
        transaction_date (datetime): The date and time of the transaction.
        transaction_type (str): The type of transaction ("auction" or "buy_now").
        amount (float): The transaction amount.
        payment_method (str): The method used for payment.
        status (str): The status of the transaction (e.g., pending, completed, canceled).
        shipping_address (str): The shipping address for the order.
        tracking_number (str, optional): The tracking number for shipment.
        created_at (datetime, optional): The creation timestamp.
        updated_at (datetime, optional): The last updated timestamp.
    """
    def __init__(
            self,
            listing_id: int,
            buyer_id: int,
            seller_id: int,
            transaction_date: datetime,
            transaction_type: str,  # "auction" or "buy_now"
            amount: float,
            payment_method: str,
            status: str,  # e.g., "pending", "completed", "canceled"
            shipping_address: str,
            tracking_number: str | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            transaction_id: int | None = None
    ):
        self.transaction_id = transaction_id
        self.listing_id = listing_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.transaction_date = transaction_date.strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_type = transaction_type
        self.amount = amount
        self.payment_method = payment_method
        self.status = status
        self.shipping_address = shipping_address
        self.tracking_number = tracking_number
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
            "payment_method": self.payment_method,
            "status": self.status,
            "shipping_address": self.shipping_address,
            "tracking_number": self.tracking_number,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
