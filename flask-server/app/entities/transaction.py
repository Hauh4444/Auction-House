from datetime import datetime


class Transaction:
    """
    Represents a transaction in the system.

    Attributes:
        transaction_id (int, optional): The unique identifier for the transaction.
        order_id (int): The ID of the order involved in the transaction.
        transaction_date (datetime, optional): The date and time when the transaction occurred.
        transaction_type (str): The type of transaction ("auction" or "buy_now").
        amount (float): The amount of money involved in the transaction (excluding shipping).
        shipping_cost (float): The cost of shipping associated with the transaction.
        payment_method (str): The method used for payment (e.g., credit card, PayPal).
        payment_status (str): The current payment status ("pending", "completed", "failed", "refunded").
        created_at (datetime, optional): The timestamp when the transaction was created. Defaults to the current time if not provided.
        updated_at (datetime, optional): The timestamp when the transaction was last updated. Defaults to the current time if not provided.
    """
    def __init__(
            self,
            order_id: int,
            user_id: int,
            transaction_type: str, # "auction", "buy_now"
            amount: float | int,
            shipping_cost: float | int,
            payment_method: str,
            payment_status: str, # "pending", "completed", "failed", "refunded"
            transaction_date: datetime | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            transaction_id: int | None = None
    ):
        self.VALID_TRANSACTION_TYPES = {"auction", "buy_now"}
        self.VALID_PAYMENT_STATUSES = {"pending", "completed", "failed", "refunded"}

        # Type checks for required attributes
        if not isinstance(order_id, int):
            raise TypeError(f"order_id must be a int, got {type(order_id).__name__}")
        if not isinstance(user_id, int):
            raise TypeError(f"user_id must be a int, got {type(user_id).__name__}")
        if not isinstance(transaction_type, str):
            raise TypeError(f"transaction_type must be a str, got {type(transaction_type).__name__}")
        if not isinstance(amount, (float, int)):
            raise TypeError(f"amount must be a number, got {type(amount).__name__}")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError(f"shipping_cost must be a number, got {type(shipping_cost).__name__}")
        if not isinstance(payment_method, str):
            raise TypeError(f"payment_method must be a str, got {type(payment_method).__name__}")
        if not isinstance(payment_status, str):
            raise TypeError(f"payment_status must be a str, got {type(payment_status).__name__}")

        # Type checks for optional attributes
        if transaction_date is not None and not isinstance(transaction_date, datetime):
            raise TypeError(f"transaction_date must be a datetime or None, got {type(transaction_date).__name__}")
        if created_at is not None and not isinstance(created_at, (datetime, str)):
            raise TypeError(f"created_at must be a datetime or None, got {type(created_at).__name__}")
        if updated_at is not None and not isinstance(updated_at, (datetime, str)):
            raise TypeError(f"updated_at must be a datetime or None, got {type(updated_at).__name__}")
        if transaction_id is not None and not isinstance(transaction_id, int):
            raise TypeError(f"transaction_id must be a int or None, got {type(transaction_id).__name__}")

        # Value checks
        if transaction_type not in self.VALID_TRANSACTION_TYPES:
            raise ValueError(f"Listing type must be one of {self.VALID_TRANSACTION_TYPES}, got '{transaction_type}' instead")
        if payment_status not in self.VALID_PAYMENT_STATUSES:
            raise ValueError(f"Listing type must be one of {self.VALID_PAYMENT_STATUSES}, got '{payment_status}' instead")

        self.transaction_id = transaction_id
        self.order_id = order_id
        self.user_id = user_id
        self.transaction_date = transaction_date or datetime.now()
        self.transaction_type = transaction_type
        self.amount = amount
        self.shipping_cost = shipping_cost
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        """Converts the transaction object to a dictionary representation."""
        return {
            "transaction_id": self.transaction_id,
            "order_id": self.order_id,
            "user_id": self.user_id,
            "transaction_date": self.transaction_date,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "shipping_cost": self.shipping_cost,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
