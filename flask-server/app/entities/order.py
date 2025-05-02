from dataclasses import dataclass
from datetime import datetime


@dataclass
class Order:
    """
    Represents an order record in the system.

    Attributes:
        order_id (int): The unique identifier for the order in the database.
        user_id (int): The user who placed the order.
        order_number (str): The custom reference number for the order.
        total_price (float): The total price of the order.
        order_status (str): The current status of the order (e.g., PAID, SHIPPED).
        shippo_order_id (str): The unique identifier for the order in Shippo.
    """
    order_id: int
    user_id: int
    order_number: str
    total_price: float
    order_status: str
    shippo_order_id: str
