from dataclasses import dataclass
from datetime import datetime


@dataclass
class Order:
    """
    Represents an order record in the system.

    Attributes:
        order_id (int): The unique identifier for the order.
        user_id (int): The user who placed the order.
        total_price (float): The total price of the order.
    """
    order_id: int
    user_id: int
    total_price: float
