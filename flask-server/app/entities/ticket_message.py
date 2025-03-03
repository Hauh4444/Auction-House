from dataclasses import dataclass
from datetime import datetime


@dataclass
class TicketMessage:
    """
    Represents a message in a support ticket.

    Attributes:
        message_id (int, optional): The unique identifier for the message.
        ticket_id (int): The ID of the associated support ticket.
        user_sender_id (int, optional): The ID of the user who sent the message (if applicable).
        staff_sender_id (int, optional): The ID of the staff member who sent the message (if applicable).
        message (str): The content of the message.
        sent_at (datetime, optional): The timestamp when the message was sent.
    """
    def __init__(
            self,
            ticket_id: int,
            message: str,
            user_sender_id: int | None = None,
            staff_sender_id: int | None = None,
            sent_at: datetime | None = None,
            message_id: int | None = None
    ):
        self.message_id = message_id
        self.ticket_id = ticket_id
        self.user_sender_id = user_sender_id
        self.staff_sender_id = staff_sender_id
        self.message = message
        self.sent_at = sent_at or datetime.now()

    def to_dict(self):
        """Converts the ticket message object to a dictionary representation."""
        return {
            "message_id": self.message_id,
            "ticket_id": self.ticket_id,
            "user_sender_id": self.user_sender_id,
            "staff_sender_id": self.staff_sender_id,
            "message": self.message,
            "sent_at": self.sent_at
        }
