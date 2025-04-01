from dataclasses import dataclass
from datetime import datetime


@dataclass
class SupportTicket:
    """
    Represents a support ticket in the system.

    Attributes:
        ticket_id (int, optional): The unique identifier for the support ticket.
        user_id (int): The ID of the user who created the ticket.
        subject (str): The subject of the support ticket.
        status (str): The status of the ticket (e.g., "Open", "Closed", "In Progress").
        priority (str): The priority level of the ticket (e.g., "Low", "Medium", "High").
        assigned_to (int, optional): The ID of the assigned support staff.
        created_at (datetime, optional): The timestamp when the ticket was created.
        updated_at (datetime, optional): The timestamp when the ticket was last updated.
    """
    def __init__(
            self,
            user_id: int,
            subject: str,
            status: str,
            priority: str,
            assigned_to: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            ticket_id: int | None = None
    ):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.subject = subject
        self.status = status
        self.priority = priority
        self.assigned_to = assigned_to
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        """Converts the support ticket object to a dictionary representation."""
        return {
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "subject": self.subject,
            "status": self.status,
            "priority": self.priority,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
