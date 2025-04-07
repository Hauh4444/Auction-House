from pymysql import cursors

from ..database.connection import get_db
from ..entities import TicketMessage


class TicketMessageMapper:
    @staticmethod
    def get_messages_by_ticket_id(ticket_id, db_session=None):
        """
        Retrieve all messages for a given support ticket.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM ticket_messages WHERE ticket_id = %s ORDER BY sent_at ASC", (ticket_id,))
        messages = cursor.fetchall()
        return [TicketMessage(**message).to_dict() for message in messages]


    @staticmethod
    def create_message(data, db_session=None):
        """
        Create a new ticket message.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO ticket_messages (ticket_id, sender_id, message, sent_at)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(statement, tuple(TicketMessage(**data).to_dict().values())[1:]) # Exclude message_id
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_message(message_id, updates, db_session=None):
        """
        Update a ticket message's details.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        update_clause = ", ".join(f"{key} = %s" for key in updates.keys())
        values = list(updates.values()) + [message_id]
        cursor.execute(f"UPDATE ticket_messages SET {update_clause} WHERE message_id = %s", values)
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_message(message_id, db_session=None):
        """
        Delete a ticket message by its ID.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM ticket_messages WHERE message_id = %s", (message_id,))
        db.commit()
        return cursor.rowcount