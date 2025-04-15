from dataclasses import dataclass
from datetime import datetime


@dataclass
class Order:
    """
    Represents an order in the system.

    Attributes:
        order_id (int, optional): The unique identifier for the order.
        user_id (int): The ID of the user who placed the order.
        order_date (datetime): The date and time when the order was placed.
        status (str): The current status of the order (e.g., pending, processing, shipped, delivered, cancelled, returned).
        created_at (datetime, optional): The timestamp when the order was created. Defaults to the current time if not provided.
        updated_at (datetime, optional): The timestamp of the last update to the order. Defaults to the current time if not provided.
    """
    def __init__(
            self,
            user_id: int,
            order_date: datetime,
            status: str,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            order_id: int | None = None
    ):
        self.VALID_STATUSES = {"pending", "processing", "shipped", "delivered", "cancelled", "returned"}

        # Type checks

        # Value checks
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Listing type must be one of {self.VALID_STATUSES}, got '{status}' instead")

        self.order_id = order_id
        self.user_id = user_id
        self.order_date = order_date
        self.status = status
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts the order object to a dictionary representation."""
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "order_date": self.order_date,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
