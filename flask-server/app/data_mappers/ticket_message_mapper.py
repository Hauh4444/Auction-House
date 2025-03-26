from datetime import datetime

from ..database.connection import get_db
from ..entities import TicketMessage


class TicketMessageMapper:
    @staticmethod
    def get_message_by_id(message_id, db_session=None):
        """
        Retrieve a ticket message by its ID.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM ticket_messages WHERE message_id = ?", (message_id,))
        message = cursor.fetchone()
        return TicketMessage(**message).to_dict() if message else None

    @staticmethod
    def get_messages_by_ticket_id(ticket_id, db_session=None):
        """
        Retrieve all messages for a given support ticket.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM ticket_messages WHERE ticket_id = ? ORDER BY sent_at ASC", (ticket_id,))
        messages = cursor.fetchall()
        return [TicketMessage(**message).to_dict() for message in messages]

    @staticmethod
    def create_message(data, db_session=None):
        """
        Create a new ticket message.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO ticket_messages (ticket_id, user_sender_id, staff_sender_id, message, sent_at)
            VALUES (?, ?, ?, ?, ?)
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
        cursor = db.cursor()
        update_clause = ", ".join(f"{key} = ?" for key in updates.keys())
        values = list(updates.values()) + [message_id]
        cursor.execute(f"UPDATE ticket_messages SET {update_clause} WHERE message_id = ?", values)
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_message(message_id, db_session=None):
        """
        Delete a ticket message by its ID.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM ticket_messages WHERE message_id = ?", (message_id,))
        db.commit()
        return cursor.rowcount
