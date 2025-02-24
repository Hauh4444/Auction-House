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
        self.message_id = message_id
        self.sender_id = sender_id
        self.chat_id = chat_id
        self.message = message
        self.sent_at = sent_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts the chat message object to a dictionary representation."""
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "chat_id": self.chat_id,
            "content": self.message,
            "created_at": self.sent_at
        }
