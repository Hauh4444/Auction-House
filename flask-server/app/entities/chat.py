from dataclasses import dataclass
from datetime import datetime


@dataclass
class Chat:
    """
    Represents a chat in the system.

    Attributes:
        chat_id (int, optional): The unique identifier for the chat.
        user1_id (int): The ID of the first user in the chat.
        user2_id (int): The ID of the second user in the chat.
        created_at (datetime, optional): The creation timestamp.
    """

    def __init__(
            self,
            user1_id: int,
            user2_id: int,
            created_at: datetime | None = None,
            chat_id: int | None = None
    ):
        if not isinstance(user1_id, int):
            raise TypeError("user1_id must be a int")
        if not isinstance(user2_id, int):
            raise TypeError("user2_id must be a int")
        if created_at is not None and not isinstance(created_at, datetime) and not isinstance(created_at, str):
            raise TypeError("created_at must be a datetime or None")
        if chat_id is not None and not isinstance(chat_id, int):
            raise TypeError("chat_id must be an int or None")

        self.chat_id = chat_id
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts the chat object to a dictionary representation."""
        return {
            "chat_id": self.chat_id,
            "user1_id": self.user1_id,
            "user2_id": self.user2_id,
            "created_at": self.created_at
        }
