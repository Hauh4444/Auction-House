from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderItem:
    """
    Represents an order in the system.

    Attributes:
        order_item_id (int): The unique identifier for the order item.
        order_id (int, optional): The ID of the order that the order item is in.
        listing_id (int): The ID of the listing associated with the item.
        quantity (int): The quantity of the purchased item.
        price (float): The price of the purchased item.
        total_price (float): The total price of the order item.
        created_at (datetime, optional): The timestamp when the order was created. Defaults to the current time if not provided.
        updated_at (datetime, optional): The timestamp of the last update to the order. Defaults to the current time if not provided.
    """
    def __init__(
            self,
            order_id: int,
            listing_id: int,
            quantity: int,
            price: float,
            total_price: float,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            order_item_id: int | None = None
    ):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.listing_id = listing_id
        self.quantity = quantity
        self.price = price
        self.total_price = total_price
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        """Converts the order object to a dictionary representation."""
        return {
            "order_item_id": self.order_item_id,
            "order_id": self.order_id,
            "listing_id": self.listing_id,
            "quantity": self.quantity,
            "price": self.price,
            "total_price": self.total_price,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
