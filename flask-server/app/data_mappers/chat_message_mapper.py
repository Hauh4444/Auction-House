from pymysql import cursors

from ..database.connection import get_db
from ..entities import ChatMessage


class ChatMessagesMapper:
    @staticmethod
    def get_messages_by_chat_id(chat_id, db_session=None):
        """
        Retrieve all messages for a given chat.

        Args:
            chat_id (int): The ID of the chat.
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of chat message dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM chat_messages WHERE chat_id = %s ORDER BY sent_at", (chat_id,))
        messages = cursor.fetchall()
        return [ChatMessage(**message).to_dict() for message in messages]


    @staticmethod
    def get_message_by_id(message_id, db_session=None):
        """
        Retrieve a specific message by its ID.

        Args:
            message_id (int): The ID of the message.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Chat message details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM chat_messages WHERE message_id = %s", (message_id,))
        message = cursor.fetchone()
        return ChatMessage(**message).to_dict() if message else None


    @staticmethod
    def create_message(data, db_session=None):
        """
        Create a new chat message.

        Args:
            data (dict): Dictionary containing message details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created message.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO chat_messages (sender_id, chat_id, content, created_at) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(statement, tuple(ChatMessage(**data).to_dict().values())[1:]) # Exclude message_id (auto-incremented)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def delete_message(message_id, db_session=None):
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
        cursor.execute("DELETE FROM chat_messages WHERE message_id = %s", (message_id,))
        db.commit()
        return cursor.rowcount
