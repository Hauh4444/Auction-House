from datetime import datetime

from ..database import get_db
from ..entities import SupportTicket


class SupportTicketMapper:
    """Handles database operations related to support tickets."""
    @staticmethod
    def get_ticket_by_id(ticket_id, db_session=None):
        """Retrieve a support ticket by its ID.

        Args:
            ticket_id (int): The ID of the support ticket.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Support ticket details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM support_tickets WHERE ticket_id = ?", (ticket_id,))
        ticket = cursor.fetchone()
        return SupportTicket(**ticket).to_dict() if ticket else None


    @staticmethod
    def get_tickets_by_user_id(user_id, db_session=None):
        """Retrieve all support tickets for a given user.

        Args:
            user_id (int): The ID of the user.
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of support ticket dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM support_tickets WHERE user_id = ?", (user_id,))
        tickets = cursor.fetchall()
        return [SupportTicket(**ticket).to_dict() for ticket in tickets]


    @staticmethod
    def create_ticket(data, db_session=None):
        """Create a new support ticket.

        Args:
            data (dict): Dictionary containing support ticket details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created ticket.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO support_tickets (user_id, order_id, subject, status, priority, assigned_to, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(SupportTicket(**data).to_dict().values())[1:]) # Exclude ticket_id (auto-incremented)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_ticket(ticket_id, updates, db_session=None):
        """Update a support ticket's details.

        Args:
            ticket_id (int): The ID of the ticket to update.
            updates (dict): A dictionary of the fields to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        update_clause = ", ".join(f"{key} = ?" for key in updates.keys())
        values = list(updates.values()) + [ticket_id]
        cursor.execute(f"UPDATE support_tickets SET {update_clause}, updated_at = ? WHERE ticket_id = ?", (*values, datetime.now()))
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_ticket(ticket_id, db_session=None):
        """Delete a support ticket by its ID.

        Args:
            ticket_id (int): The ID of the ticket to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM support_tickets WHERE ticket_id = ?", (ticket_id,))
        db.commit()
        return cursor.rowcount
