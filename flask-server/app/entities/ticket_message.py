from datetime import datetime


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
        if not isinstance(ticket_id, int):
            raise TypeError("ticket_id must be an int")
        if not isinstance(sender_id, int):
            raise TypeError("sender_id must be an int")
        if not isinstance(message, str):
            raise TypeError("message must be a str")
        if sent_at is not None and not isinstance(sent_at, datetime):
            raise TypeError("sent_at must be a datetime or None")
        if message_id is not None and not isinstance(message_id, int):
            raise TypeError("message_id must be an int or None")

        self.message_id = message_id
        self.ticket_id = ticket_id
        self.sender_id = sender_id
        self.message = message
        self.sent_at = sent_at or datetime.now()

    def to_dict(self):
        """Converts the ticket message object to a dictionary representation."""
        return {
            "message_id": self.message_id,
            "ticket_id": self.ticket_id,
            "sender_id": self.sender_id,
            "message": self.message,
            "sent_at": self.sent_at
        }
