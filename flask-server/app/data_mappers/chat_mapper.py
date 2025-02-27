from ..database import get_db
from ..entities.chat import Chat


class ChatMapper:
    """Handles database operations related to chats."""

    @staticmethod
    def get_all_chats(session=None):
        """Retrieve all chats from the database.

        Args:
            session: Optional database session to be used in tests.

        Returns:
            list: A list of chat dictionaries.
        """
        db = session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM chats")
        chats = cursor.fetchall()
        return [Chat(**chat).to_dict() for chat in chats]

    @staticmethod
    def get_chat_by_id(chat_id, session=None):
        """Retrieve a chat by its ID.

        Args:
            chat_id (int): The ID of the chat to retrieve.
            session: Optional database session to be used in tests.

        Returns:
            dict: Chat details if found, otherwise None.
        """
        db = session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM chats WHERE chat_id = ?", (chat_id,))
        chat = cursor.fetchone()
        return Chat(**chat).to_dict() if chat else None

    @staticmethod
    def create_chat(data, session=None):
        """Create a new chat in the database.

        Args:
            data (dict): Dictionary containing chat details.
            session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created chat.
        """
        db = session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO chats (user1_id, user2_id, created_at) 
            VALUES (?, ?, ?)
        """
        cursor.execute(statement, tuple(Chat(**data).to_dict().values())[1:]) # Exclude chat_id (auto-incremented)
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def delete_chat(chat_id, session=None):
        """Delete a chat by its ID.

        Args:
            chat_id (int): The ID of the chat to delete.
            session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = session or get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM chats WHERE chat_id = ?", (chat_id,))
        db.commit()
        return cursor.rowcount

