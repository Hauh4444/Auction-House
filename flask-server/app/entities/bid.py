from datetime import datetime


class Bid:
    """
    Represents a bid in the system.

    Attributes:
        bid_id (int, optional): The unique identifier for the bid.
        listing_id (int): The ID of the listing that the bid is for.
        user_id (int): The ID of the user who made the bid.
        amount (float): The amount of the bid.
        created_at (datetime, optional): The creation timestamp.
    """
    def __init__(
            self,
            listing_id: int,
            user_id: int,
            amount: float | int,
            created_at: datetime | None = None,
            bid_id: int | None = None,
    ):
        # Type checks for required attributes
        if not isinstance(listing_id, int):
            raise TypeError(f"listing_id must be a int, got {type(listing_id).__name__}")
        if not isinstance(user_id, int):
            raise TypeError(f"user_id must be a int, got {type(user_id).__name__}")
        if not isinstance(amount, (float, int)):
            raise TypeError(f"amount must be a number, got {type(amount).__name__}")

        # Type checks for optional attributes
        if created_at is not None and not isinstance(created_at, (datetime, str)):
            raise TypeError(f"created_at must be a datetime or None, got {type(created_at).__name__}")
        if bid_id is not None and not isinstance(bid_id, int):
            raise TypeError(f"bid_id must be a int or None, got {type(bid_id).__name__}")

        self.bid_id = bid_id
        self.listing_id = listing_id
        self.user_id = user_id
        self.amount = amount
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        """Converts the bid object to a dictionary representation."""
        return {
            "bid_id": self.bid_id,
            "listing_id": self.listing_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "created_at": self.created_at
        }

