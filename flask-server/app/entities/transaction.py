from datetime import datetime


class Transaction:
    """
    Represents a transaction in the system.

    Attributes:
        transaction_id (int, optional): The unique identifier for the transaction.
        user_id (int): The ID of the user.
        payment_intent_id (str): Payment Intent ID.
        created_at (datetime, optional): The timestamp when the transaction was created. Defaults to the current time if not provided.
        updated_at (datetime, optional): The timestamp when the transaction was last updated. Defaults to the current time if not provided.
    """
    def __init__(
            self,
            user_id: int,
            payment_intent_id: str,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            transaction_id: int | None = None
    ):
        self.VALID_TRANSACTION_TYPES = {"auction", "buy_now"}
        self.VALID_PAYMENT_STATUSES = {"pending", "completed", "failed", "refunded"}

        # Type checks for required attributes
        if not isinstance(user_id, int):
            raise TypeError(f"user_id must be a int, got {type(user_id).__name__}")
        if not isinstance(payment_intent_id, str):
            raise TypeError(f"payment_intent_id must be a str, got {type(payment_intent_id).__name__}")

        # Type checks for optional attributes
        if created_at is not None and not isinstance(created_at, (datetime, str)):
            raise TypeError(f"created_at must be a datetime or None, got {type(created_at).__name__}")
        if updated_at is not None and not isinstance(updated_at, (datetime, str)):
            raise TypeError(f"updated_at must be a datetime or None, got {type(updated_at).__name__}")
        if transaction_id is not None and not isinstance(transaction_id, int):
            raise TypeError(f"transaction_id must be a int or None, got {type(transaction_id).__name__}")

        self.transaction_id = transaction_id
        self.user_id = user_id
        self.payment_intent_id = payment_intent_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        """Converts the transaction object to a dictionary representation."""
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "payment_intent_id": self.payment_intent_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
