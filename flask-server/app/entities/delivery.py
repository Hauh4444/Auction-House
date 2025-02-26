from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class Delivery:
    """
    Represents a delivery record in the system.

    Attributes:
        delivery_id (int, optional): The unique identifier for the delivery.
        order_id (int): The order associated with this delivery.
        user_id (int): The user who placed the order.
        address (str): The delivery address.
        city (str): The city of delivery.
        state (str): The state of delivery.
        postal_code (str): The postal code of the delivery address.
        country (str): The country of delivery.
        delivery_status (str): The current status of the delivery.
        tracking_number (str, optional): The tracking number for the delivery.
        courier (str, optional): The courier handling the delivery.
        estimated_delivery_date (date, optional): The estimated delivery date.
        delivered_at (datetime, optional): The actual delivery timestamp.
        created_at (datetime, optional): The creation timestamp.
        updated_at (datetime, optional): The last updated timestamp.
    """
    def __init__(
            self,
            order_id: int,
            user_id: int,
            address: str,
            city: str,
            state: str,
            postal_code: str,
            country: str,
            delivery_status: str,
            tracking_number: str | None = None,
            courier: str | None = None,
            estimated_delivery_date: date | None = None,
            delivered_at: datetime | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            delivery_id: int | None = None
    ):
        self.delivery_id = delivery_id
        self.order_id = order_id
        self.user_id = user_id
        self.address = address
        self.city = city
        self.state = state
        self.postal_code = postal_code
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
            "order_id": self.order_id,
            "user_id": self.user_id,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "country": self.country,
            "delivery_status": self.delivery_status,
            "tracking_number": self.tracking_number,
            "courier": self.courier,
            "estimated_delivery_date": self.estimated_delivery_date.strftime("%Y-%m-%d") if self.estimated_delivery_date else None,
            "delivered_at": self.delivered_at.strftime("%Y-%m-%d %H:%M:%S") if self.delivered_at else None,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
