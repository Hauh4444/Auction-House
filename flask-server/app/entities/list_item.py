from dataclasses import dataclass
from datetime import datetime


@dataclass
class ListItem:
    """
    Represents a list item in the system.
    """
    def __init__(
            self,
            list_id: int,
            listing_id: str,
            created_at: datetime | None = None,
            list_item_id: int | None = None
    ):
        self.list_item_id = list_item_id
        self.list_id = list_id
        self.listing_id = listing_id
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts the list item object to a dictionary representation."""
        return {
            "list_item_id": self.list_item_id,
            "list_id": self.list_id,
            "listing_id": self.listing_id,
            "created_at": self.created_at
        }
