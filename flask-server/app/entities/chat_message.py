from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatMessage:
    """
    Represents a chat message in the system.

    Attributes:
        message_id (int, optional): The unique identifier for the message.
        sender_id (int): The ID of the user who sent the message.
        chat_id (int): The ID of the chat the message belongs to.
        message (str): The content of the message.
        sent_at (datetime, optional): The creation timestamp.
    """
    def __init__(
            self,
            sender_id: int,
            chat_id: int,
            message: str,
            sent_at: datetime | None = None,
            message_id: int | None = None
    ):
        # Type checks for required attributes
        if not isinstance(sender_id, int):
            raise TypeError(f"sender_id must be a int, got {type(sender_id).__name__}")
        if not isinstance(chat_id, int):
            raise TypeError(f"chat_id must be a int, got {type(chat_id).__name__}")
        if not isinstance(message, str):
            raise TypeError(f"message must be a str, got {type(message).__name__}")

        # Type checks for optional attributes
        if sent_at is not None and not isinstance(sent_at, (datetime, str)):
            raise TypeError(f"sent_at must be a datetime,, or None, got {type(sent_at).__name__}")
        if message_id is not None and not isinstance(message_id, int):
            raise TypeError(f"message_id must be an int or None, got {type(message_id).__name__}")

        self.message_id = message_id
        self.sender_id = sender_id
        self.chat_id = chat_id
        self.message = message
        self.sent_at = sent_at or datetime.now()

    def to_dict(self):
        """Converts the chat message object to a dictionary representation."""
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "chat_id": self.chat_id,
            "message": self.message,
            "sent_at": self.sent_at
        }
