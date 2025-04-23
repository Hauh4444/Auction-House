from datetime import datetime


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
            updated_at: datetime | None = None,
            chat_id: int | None = None
    ):
        # Type checks for required attributes
        if not isinstance(user1_id, int):
            raise TypeError(f"user1_id must be a int, got {type(user1_id).__name__}")
        if not isinstance(user2_id, int):
            raise TypeError(f"user2_id must be a int, got {type(user2_id).__name__}")

        # Type checks for optional attributes
        if created_at is not None and not isinstance(created_at, (datetime, str)):
            raise TypeError(f"created_at must be a datetime,, or None, got {type(created_at).__name__}")
        if updated_at is not None and not isinstance(updated_at, (datetime, str)):
            raise TypeError(f"updated_at must be a datetime,, or None, got {type(updated_at).__name__}")
        if chat_id is not None and not isinstance(chat_id, int):
            raise TypeError(f"chat_id must be an int or None, got {type(chat_id).__name__}")

        self.chat_id = chat_id
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.created_at = created_at or datetime.now()
        self.updated_at = created_at or datetime.now()

    def to_dict(self):
        """Converts the chat object to a dictionary representation."""
        return {
            "chat_id": self.chat_id,
            "user1_id": self.user1_id,
            "user2_id": self.user2_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
