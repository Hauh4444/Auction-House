from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class Delivery:
    """
    Represents a delivery record in the system.

    Attributes:
        delivery_id (int): The unique identifier for the delivery.
        user_id (int): The user who placed the order.
        tracking_number (str): The tracking number for the delivery.
        courier (str): The courier handling the delivery.
        tracking_url_provider (str): The URL to track the shipment.
    """
    delivery_id: int
    user_id: int
    tracking_number: str
    courier: str
    tracking_url_provider: str

    def __init__(
            self,
            order_item_id: int,
            user_id: int,
            address: str,
            city: str,
            state: str,
            country: str,
            delivery_status: str,  # "pending", "processing", "shipped", "in_transit", "out_for_delivery", "delivered", "cancelled", "returned", "failed"
            tracking_number: str | None = None,
            courier: str | None = None,
            estimated_delivery_date: date | None = None,
            delivered_at: datetime | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            delivery_id: int | None = None
    ):
        self.VALID_DELIVERY_STATUSES = {"pending", "processing", "shipped", "in_transit", "out_for_delivery", "delivered", "cancelled", "returned", "failed"}

        # Type checks for required attributes
        if not isinstance(order_item_id, int):
            raise TypeError(f"order_id must be an int, got {type(order_item_id).__name__}")
        if not isinstance(user_id, int):
            raise TypeError(f"user_id must be an int, got {type(user_id).__name__}")
        if not isinstance(address, str):
            raise TypeError(f"address must be a str, got {type(address).__name__}")
        if not isinstance(city, str):
            raise TypeError(f"city must be a str, got {type(city).__name__}")
        if not isinstance(state, str):
            raise TypeError(f"state must be a str, got {type(state).__name__}")
        if not isinstance(country, str):
            raise TypeError(f"country must be a str, got {type(country).__name__}")
        if not isinstance(delivery_status, str):
            raise TypeError(f"delivery_status must be a str, got {type(delivery_status).__name__}")

        # Type checks for optional attributes
        if tracking_number is not None and not isinstance(tracking_number, str):
            raise TypeError(f"tracking_number must be a str, got {type(tracking_number).__name__}")
        if courier is not None and not isinstance(courier, str):
            raise TypeError(f"courier must be a str, got {type(courier).__name__}")
        if estimated_delivery_date is not None and not isinstance(estimated_delivery_date, (date, str)):
            raise TypeError(f"estimated_delivery_date must be a date, str, or None, got {type(estimated_delivery_date).__name__}")
        if delivered_at is not None and not isinstance(delivered_at, (datetime, str)):
            raise TypeError(f"delivered_at must be a datetime, or None, got {type(delivered_at).__name__}")
        if created_at is not None and not isinstance(created_at, (datetime, str)):
            raise TypeError(f"created_at must be a datetime, or None, got {type(created_at).__name__}")
        if updated_at is not None and not isinstance(updated_at, (datetime, str)):
            raise TypeError(f"updated_at must be a datetime, or None, got {type(updated_at).__name__}")

        # Value checks for enumerated attributes
        if delivery_status not in self.VALID_DELIVERY_STATUSES:
            raise ValueError(f"delivery_status must be one of {self.VALID_DELIVERY_STATUSES}, got '{delivery_status}' instead")

        self.delivery_id = delivery_id
        self.order_item_id = order_item_id
        self.user_id = user_id
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.delivery_status = delivery_status
        self.tracking_number = tracking_number
        self.courier = courier
        self.estimated_delivery_date = estimated_delivery_date
        self.delivered_at = delivered_at
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts the delivery object to a dictionary representation."""
        return {
            "delivery_id": self.delivery_id,
            "order_item_id": self.order_item_id,
            "user_id": self.user_id,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "delivery_status": self.delivery_status,
            "tracking_number": self.tracking_number,
            "courier": self.courier,
            "estimated_delivery_date": self.estimated_delivery_date.strftime("%Y-%m-%d %H:%M:%S") if self.estimated_delivery_date else None,
            "delivered_at": self.delivered_at,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
