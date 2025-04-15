from pymysql import cursors
from datetime import datetime

from ..database.connection import get_db
from ..entities import SupportTicket


class SupportTicketMapper:
    @staticmethod
    def get_tickets_by_user_id(user_id, db_session=None):
        """
        Retrieve all support tickets for a given user.

        Args:
            user_id (int): The ID of the user.
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of support ticket dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM support_tickets WHERE user_id = %s ORDER BY updated_at DESC", (user_id,))
        tickets = cursor.fetchall()
        return [SupportTicket(**ticket).to_dict() for ticket in tickets]


    @staticmethod
    def get_tickets_by_staff_id(staff_id, db_session=None):
        """
        Retrieve all support tickets for a given user.

        Args:
            staff_id (int): The ID of the user.
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of support ticket dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM support_tickets WHERE assigned_to = %s ORDER BY updated_at DESC", (staff_id,))
        tickets = cursor.fetchall()
        return [SupportTicket(**ticket).to_dict() for ticket in tickets]


    @staticmethod
    def get_ticket_by_id(ticket_id, db_session=None):
        """
        Retrieve a support ticket by its ID.

        Args:
            ticket_id (int): The ID of the support ticket.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: StaffSupport ticket details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM support_tickets WHERE ticket_id = %s", (ticket_id,))
        ticket = cursor.fetchone()
        return SupportTicket(**ticket).to_dict() if ticket else None


    @staticmethod
    def create_ticket(data, db_session=None):
        """
        Create a new support ticket.

        Args:
            data (dict): Dictionary containing support ticket details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created ticket.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO support_tickets (user_id, subject, status, priority, assigned_to, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(statement, tuple(SupportTicket(**data).to_dict().values())[1:]) # Exclude ticket_id (auto-incremented)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_ticket(ticket_id, data, db_session=None):
        """
        Update a support ticket's details.

        Args:
            ticket_id (int): The ID of the ticket to update.
            data (dict): A dictionary of the fields to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        update_clause = ", ".join(f"{key} = %s" for key in data.keys())
        values = list(data.values()) + [ticket_id]
        cursor.execute(f"UPDATE support_tickets SET {update_clause}, updated_at = %s WHERE ticket_id = %s", (*values, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
        return cursor.rowcount


    @staticmethod
    def update_ticket_timestamp(ticket_id, db_session=None):
        """
        Update a support ticket's timestamp.

        Args:
            ticket_id (int): The ID of the ticket to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute(f"UPDATE support_tickets SET updated_at = %s WHERE ticket_id = %s", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ticket_id))
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_ticket(ticket_id, db_session=None):
        """
        Delete a support ticket by its ID.

        Args:
            ticket_id (int): The ID of the ticket to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM support_tickets WHERE ticket_id = %s", (ticket_id,))
        db.commit()
        return cursor.rowcount
