from pymysql import cursors
from datetime import datetime

from ..database.connection import get_db
from ..entities import User


class AuthMapper:
    @staticmethod
    def get_user_by_id(user_id, db_session=None):
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: User details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore

        # Check in users table
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        return User(**user).to_dict() if user else None


    @staticmethod
    def get_user_by_username(username, db_session=None):
        """
        Retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            Object: User details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore

        # Check in users table
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        return User(**user) if user else None


    @staticmethod
    def create_user(data, db_session=None):
        """
        Create a new user in the database.

        Args:
            data (dict): Dictionary containing user details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created user.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        statement = """
            INSERT INTO users (role, username, password_hash, email, created_at, updated_at, last_login, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(statement, tuple(User(**data).to_dict().values())[1:])
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_last_login(user_id, db_session=None):
        """
        Update the last login timestamp for a user.

        Args:
            user_id (int): The ID of the user to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore

        statement = "UPDATE users SET last_login = %s WHERE user_id = %s"

        cursor.execute(statement, (datetime.now(), user_id))
        db.commit()
        return cursor.rowcount