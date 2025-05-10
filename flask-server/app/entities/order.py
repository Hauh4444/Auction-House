from datetime import datetime


class Order:
    """
    Represents an order in the system.

    Attributes:
        order_id (int, optional): The unique identifier for the order.
        user_id (int): The ID of the user who placed the order.
        order_date (datetime, optional): The date and time when the order was placed.
        status (str): The current status of the order (e.g., pending, processing, shipped, delivered, cancelled, returned).
        created_at (datetime, optional): The timestamp when the order was created. Defaults to the current time if not provided.
        updated_at (datetime, optional): The timestamp of the last update to the order. Defaults to the current time if not provided.
    """
    def __init__(
            self,
            user_id: int,
            status: str,
            order_date: datetime | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            order_id: int | None = None
    ):
        self.VALID_STATUSES = {"pending", "processing", "shipped", "delivered", "cancelled", "returned"}

        # Type checks for required attributes
        if not isinstance(user_id, int):
            raise TypeError(f"user_id must be a int, got {type(user_id).__name__}")
        if not isinstance(status, str):
            raise TypeError(f"status must be a str, got {type(status).__name__}")

        # Type checks for optional attributes
        if order_date is not None and not isinstance(order_date, datetime):
            raise TypeError(f"order_date must be a datetime or None, got {type(order_date).__name__}")
        if created_at is not None and not isinstance(created_at, (datetime, str)):
            raise TypeError(f"created_at must be a datetime or None, got {type(created_at).__name__}")
        if updated_at is not None and not isinstance(updated_at, (datetime, str)):
            raise TypeError(f"updated_at must be a datetime or None, got {type(updated_at).__name__}")
        if order_id is not None and not isinstance(order_id, int):
            raise TypeError(f"order_id must be a int or None, got {type(order_id).__name__}")

        # Value checks
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Listing type must be one of {self.VALID_STATUSES}, got '{status}' instead")

        self.order_id = order_id
        self.user_id = user_id
        self.order_date = order_date or datetime.now()
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

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
