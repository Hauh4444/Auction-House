from pymysql import cursors
from datetime import datetime

from ..database import get_db
from ..entities import Chat


class ChatMapper:
    @staticmethod
    def get_chats_by_user_id(user_id: int, db_session=None):
        """
        Retrieve all chats for a given user.

        Args:
            user_id (int): The ID of the user.
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of chat dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM chats WHERE user1_id = %s OR user2_id = %s ORDER BY updated_at DESC", (user_id, user_id))
        chats = cursor.fetchall()

        return [Chat(**chat).to_dict() for chat in chats]


    @staticmethod
    def get_all_chats(db_session=None):
        """
        Retrieve all chats from the database.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of chat dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM chats")
        chats = cursor.fetchall()
        return [Chat(**chat).to_dict() for chat in chats]


    @staticmethod
    def get_chat_by_id(chat_id: int, db_session=None):
        """
        Retrieve a chat by its ID.

        Args:
            chat_id (int): The ID of the chat to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: Chat details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("SELECT * FROM chats WHERE chat_id = %s", (chat_id,))
        chat = cursor.fetchone()
        return Chat(**chat).to_dict() if chat else None


    @staticmethod
    def create_chat(data: dict, db_session=None):
        """
        Create a new chat in the database.

        Args:
            data (dict): Dictionary containing chat details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created chat.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO chats (user1_id, user2_id, created_at, updated_at) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(statement, tuple(Chat(**data).to_dict().values())[1:]) # Exclude chat_id (auto-incremented)
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_chat_timestamp(chat_id: int, db_session=None):
        """
        Update a chat's timestamp.

        Args:
            chat_id (int): The ID of the chat to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute(f"UPDATE chats SET updated_at = %s WHERE chat_id = %s", (datetime.now(), chat_id))
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_chat(chat_id: int, db_session=None):
        """
        Delete a chat by its ID.

        Args:
            chat_id (int): The ID of the chat to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM chats WHERE chat_id = %s", (chat_id,))
        db.commit()
        return cursor.rowcount

