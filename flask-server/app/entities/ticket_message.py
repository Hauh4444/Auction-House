from dataclasses import dataclass
from datetime import datetime


@dataclass
class TicketMessage:
    """
    Represents a message in a support ticket.

    Attributes:
        message_id (int, optional): The unique identifier for the message.
        ticket_id (int): The ID of the associated support ticket.
        sender_id (int): The ID of the user who sent the message.
        message (str): The content of the message.
        sent_at (datetime, optional): The timestamp when the message was sent.
    """
    def __init__(
            self,
            ticket_id: int,
            message: str,
            sender_id: int,
            sent_at: datetime | None = None,
            message_id: int | None = None
    ):
        self.message_id = message_id
        self.ticket_id = ticket_id
        self.sender_id = sender_id
        self.message = message
        self.sent_at = sent_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts the ticket message object to a dictionary representation."""
        return {
            "message_id": self.message_id,
            "ticket_id": self.ticket_id,
            "sender_id": self.sender_id,
            "message": self.message,
            "sent_at": self.sent_at.strftime("%Y-%m-%d %H:%M:%S")
        }
