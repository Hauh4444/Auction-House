from pymysql import cursors

from ..database import get_db
from ..entities import TicketMessage


class TicketMessageMapper:
    @staticmethod
    def get_messages_by_ticket_id(ticket_id: int, db_session=None):
        """
        Retrieve all messages for a given ticket.

        Args:
            ticket_id (int): The ID of the ticket.
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of ticket message dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM ticket_messages WHERE ticket_id = %s ORDER BY sent_at ASC", (ticket_id,))
        messages = cursor.fetchall()
        return [TicketMessage(**message).to_dict() for message in messages]


    @staticmethod
    def create_message(data: dict, db_session=None):
        """
        Create a new ticket message.

        Args:
            data (dict): Dictionary containing message details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created ticket.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO ticket_messages (ticket_id, sender_id, message, sent_at)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(statement, tuple(TicketMessage(**data).to_dict().values())[1:])
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def delete_message(message_id: int, db_session=None):
        """
        Delete a message by its ID.

        Args:
            message_id (int): The ID of the message to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM ticket_messages WHERE message_id = %s", (message_id,))
        db.commit()
        return cursor.rowcount