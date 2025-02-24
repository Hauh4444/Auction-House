from ..database import get_db
from ..entities.chats import Chats

class ChatsMapper:
    """Handles database operations related to chats."""

    @staticmethod
    def get_all_chats():
        """Retrieve all chats from the database.

        Returns:
            list: A list of chat dictionaries.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM chats")
        chats = cursor.fetchall()
        return [Chats(**chat).to_dict() for chat in chats]

    @staticmethod
    def get_chat_by_id(chat_id):
        """Retrieve a chat by its ID.

        Args:
            chat_id (int): The ID of the chat to retrieve.

        Returns:
            dict: Chat details if found, otherwise None.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM chats WHERE chat_id = ?", (chat_id,))
        chat = cursor.fetchone()
        return Chats(**chat).to_dict() if chat else None

    @staticmethod
    def create_chat(data):
        """Create a new chat in the database.

        Args:
            data (dict): Dictionary containing chat details.

        Returns:
            int: The ID of the newly created chat.
        """
        db = get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO chats (user1_id, user2_id, created_at) 
            VALUES (?, ?, ?)
        """
        cursor.execute(statement, tuple(Chats(**data).to_dict().values())[1:])  # Exclude chat_id (auto-incremented)
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def delete_chat(chat_id):
        """Delete a chat by its ID.

        Args:
            chat_id (int): The ID of the chat to delete.

        Returns:
            int: Number of rows deleted.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM chats WHERE chat_id = ?", (chat_id,))
        db.commit()
        return cursor.rowcount
    
