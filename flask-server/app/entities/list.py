from datetime import datetime


class List:
    """
    Represents a list in the system.
    """
    def __init__(
            self,
            user_id: int,
            title: str,
            created_at: datetime | None = None,
            list_id: int | None = None
    ):
        # Type checks for required attributes
        if not isinstance(user_id, int):
            raise TypeError(f"user_id must be a int, got {type(user_id).__name__}")
        if not isinstance(title, str):
            raise TypeError(f"title must be a str, got {type(title).__name__}")

        # Type checks for optional attributes
        if created_at is not None and not isinstance(created_at, (datetime, str)):
            raise TypeError(f"created_at must be a datetime or None, got {type(created_at).__name__}")
        if list_id is not None and not isinstance(list_id, int):
            raise TypeError(f"list_id must be a int or None, got {type(list_id).__name__}")

        self.list_id = list_id
        self.user_id = user_id
        self.title = title
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        """Converts the list object to a dictionary representation."""
        return {
            "list_id": self.list_id,
            "user_id": self.user_id,
            "title": self.title,
            "created_at": self.created_at
        }
