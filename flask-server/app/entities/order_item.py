from datetime import datetime


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
            price: float | int,
            total_price: float | int,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            order_item_id: int | None = None
    ):
        # Type checks for required attributes
        if not isinstance(order_id, int):
            raise TypeError(f"order_id must be a int, got {type(order_id).__name__}")
        if not isinstance(listing_id, int):
            raise TypeError(f"listing_id must be a int, got {type(listing_id).__name__}")
        if not isinstance(quantity, int):
            raise TypeError(f"quantity must be a int, got {type(quantity).__name__}")
        if not isinstance(price, (float, int)):
            raise TypeError(f"price must be a number, got {type(price).__name__}")
        if not isinstance(total_price, (float, int)):
            raise TypeError(f"total_price must be a number, got {type(total_price).__name__}")

        # Type checks for optional attributes
        if created_at is not None and not isinstance(created_at, (datetime, str)):
            raise TypeError(f"created_at must be a datetime or None, got {type(created_at).__name__}")
        if updated_at is not None and not isinstance(updated_at, (datetime, str)):
            raise TypeError(f"updated_at must be a datetime or None, got {type(updated_at).__name__}")
        if order_item_id is not None and not isinstance(order_item_id, int):
            raise TypeError(f"order_item_id must be a int or None, got {type(order_item_id).__name__}")

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
