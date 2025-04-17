from dataclasses import dataclass
from datetime import datetime


@dataclass
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
        self.list_id = list_id
        self.user_id = user_id
        self.title = title
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts the list object to a dictionary representation."""
        return {
            "list_id": self.list_id,
            "user_id": self.user_id,
            "title": self.title,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
