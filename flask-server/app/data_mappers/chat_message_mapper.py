from ..database import get_db
from ..entities.chat_messages import Chat_Messages

class ChatMessagesMapper:
    """Handles database operations related to chat messages."""

    @staticmethod
    def get_messages_by_chat_id(chat_id):
        """Retrieve all messages for a given chat.

        Args:
            chat_id (int): The ID of the chat.

        Returns:
            list: A list of chat message dictionaries.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM chat_messages WHERE chat_id = ? ORDER BY sent_at", (chat_id,))
        messages = cursor.fetchall()
        return [Chat_Messages(**message).to_dict() for message in messages]

    @staticmethod
    def get_message_by_id(message_id):
        """Retrieve a specific message by its ID.

        Args:
            message_id (int): The ID of the message.

        Returns:
            dict: Chat message details if found, otherwise None.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM chat_messages WHERE message_id = ?", (message_id,))
        message = cursor.fetchone()
        return Chat_Messages(**message).to_dict() if message else None

    @staticmethod
    def create_message(data):
        """Create a new chat message.

        Args:
            data (dict): Dictionary containing message details.

        Returns:
            int: The ID of the newly created message.
        """
        db = get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO chat_messages (sender_id, chat_id, content, created_at) 
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Chat_Messages(**data).to_dict().values())[1:])  # Exclude message_id (auto-incremented)
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def delete_message(message_id):
        """Delete a message by its ID.

        Args:
            message_id (int): The ID of the message to delete.

        Returns:
            int: Number of rows deleted.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM chat_messages WHERE message_id = ?", (message_id,))
        db.commit()
        return cursor.rowcount
