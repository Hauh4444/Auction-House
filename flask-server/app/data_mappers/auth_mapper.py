from pymysql import cursors
from datetime import datetime
import logging

from ..database.connection import get_db
from ..entities import User

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

        # Log the query for tracking
        logging.info(f"Fetching user by ID: {user_id}")
        
        # Check in users table
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            logging.info(f"User found: {user_id}")
            return User(**user).to_dict()
        else:
            logging.warning(f"User not found: {user_id}")
            return None

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

        # Log the query for tracking
        logging.info(f"Fetching user by username: {username}")
        
        # Check in users table
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            logging.info(f"User found: {username}")
            return User(**user)
        else:
            logging.warning(f"User not found: {username}")
            return None

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

        # Log the creation attempt
        logging.info(f"Creating a new user: {data['username']}")

        statement = """
            INSERT INTO users (role, username, password_hash, email, created_at, updated_at, last_login, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(statement, tuple(User(**data).to_dict().values())[1:])
        db.commit()

        user_id = cursor.lastrowid
        logging.info(f"User created successfully with ID: {user_id}")
        return user_id

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

        # Log the update attempt
        logging.info(f"Updating last login for user: {user_id}")

        statement = "UPDATE users SET last_login = %s WHERE user_id = %s"
        cursor.execute(statement, (datetime.now(), user_id))
        db.commit()

        rows_updated = cursor.rowcount
        if rows_updated:
            logging.info(f"Last login updated successfully for user: {user_id}")
        else:
            logging.warning(f"Failed to update last login for user: {user_id}")
        
        return rows_updated
