from datetime import datetime


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
        # Type checks for required attributes
        if not isinstance(list_id, int):
            raise TypeError(f"list_id must be a int, got {type(list_id).__name__}")
        if not isinstance(listing_id, int):
            raise TypeError(f"listing_id must be a int, got {type(listing_id).__name__}")

        # Type checks for optional attributes
        if created_at is not None and not isinstance(created_at, (datetime, str)):
            raise TypeError(f"created_at must be a datetime or None, got {type(created_at).__name__}")
        if list_item_id is not None and not isinstance(list_item_id, int):
            raise TypeError(f"list_item_id must be a int or None, got {type(list_item_id).__name__}")

        self.list_item_id = list_item_id
        self.list_id = list_id
        self.listing_id = listing_id
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        """Converts the list item object to a dictionary representation."""
        return {
            "list_item_id": self.list_item_id,
            "list_id": self.list_id,
            "listing_id": self.listing_id,
            "created_at": self.created_at
        }
