from datetime import datetime


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
        # Type checks for required attributes
        if not isinstance(user_id, int):
            raise TypeError(f"user_id must be a int, got {type(user_id).__name__}")
        if not isinstance(subject, str):
            raise TypeError(f"subject must be a str, got {type(subject).__name__}")
        if not isinstance(status, str):
            raise TypeError(f"status must be a str, got {type(status).__name__}")
        if not isinstance(priority, str):
            raise TypeError(f"priority must be a str, got {type(priority).__name__}")

        # Type checks for optional attributes
        if assigned_to is not None and not isinstance(assigned_to, int):
            raise TypeError(f"assigned_to must be a int or None, got {type(assigned_to).__name__}")
        if created_at is not None and not isinstance(created_at, (datetime, str)):
            raise TypeError(f"created_at must be a datetime or None, got {type(created_at).__name__}")
        if updated_at is not None and not isinstance(updated_at, (datetime, str)):
            raise TypeError(f"updated_at must be a datetime or None, got {type(updated_at).__name__}")
        if ticket_id is not None and not isinstance(ticket_id, int):
            raise TypeError(f"ticket_id must be a int or None, got {type(ticket_id).__name__}")

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
