from dataclasses import dataclass
from datetime import datetime


@dataclass
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
            amount: float,
            created_at: datetime | None = None,
            bid_id: int | None = None,
    ):
        self.bid_id = bid_id
        self.listing_id = listing_id
        self.user_id = user_id
        self.amount = amount
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts the bid object to a dictionary representation."""
        return {
            "bid_id": self.bid_id,
            "listing_id": self.listing_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

