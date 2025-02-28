from dataclasses import dataclass
from datetime import datetime


@dataclass
class Order:
    """
    Represents an order in the system.

    Attributes:
        order_id (int, optional): The unique identifier for the order.
        user_id (int): The ID of the user who placed the order.
        order_date (datetime): The date and time the order was placed.
        status (str): The status of the order (e.g., processing, shipped, delivered).
        total_amount (float): The total amount of the order.
        payment_status (str): The payment status (e.g., paid, pending, failed).
        payment_method (str): The method used for payment.
        shipping_address (str): The shipping address.
        shipping_method (str): The chosen shipping method.
        tracking_number (str, optional): The tracking number for shipment.
        shipping_cost (float, optional): The cost of shipping.
        created_at (datetime, optional): The creation timestamp.
        updated_at (datetime, optional): The last updated timestamp.
    """
    def __init__(
            self,
            user_id: int,
            order_date: datetime,
            status: str, # "pending", "processing", "shipped", "delivered", "cancelled", "returned"
            total_amount: float,
            payment_status: str, # "pending", "completed", "failed", "refunded"
            payment_method: str,
            shipping_address: str,
            shipping_method: str,
            tracking_number: str | None = None,
            shipping_cost: float | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            order_id: int | None = None
    ):
        self.VALID_STATUSES = {"pending", "processing", "shipped", "delivered", "cancelled", "returned"}
        self.VALID_PAYMENT_STATUSES = {"pending", "completed", "failed", "refunded"}

        # Type checks

        # Value checks
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Listing type must be one of {self.VALID_STATUSES}, got '{status}' instead")
        if payment_status not in self.VALID_PAYMENT_STATUSES:
            raise ValueError(f"Listing type must be one of {self.VALID_PAYMENT_STATUSES}, got '{payment_status}' instead")

        self.order_id = order_id
        self.user_id = user_id
        self.order_date = order_date
        self.status = status
        self.total_amount = total_amount
        self.payment_status = payment_status
        self.payment_method = payment_method
        self.shipping_address = shipping_address
        self.shipping_method = shipping_method
        self.tracking_number = tracking_number
        self.shipping_cost = shipping_cost
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        """Converts the order object to a dictionary representation."""
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "order_date": self.order_date,
            "status": self.status,
            "total_amount": self.total_amount,
            "payment_status": self.payment_status,
            "payement_method": self.payment_method,
            "shipping_address": self.shipping_address,
            "shipping_method": self.shipping_method,
            "tracking_number": self.tracking_number,
            "shipping_cost": self.shipping_cost,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
