from pymysql import DatabaseError
from datetime import datetime

from ..database import get_db
from ..entities.user import User
from ..entities.staff_user import StaffUser


class AuthMapper:
    """Handles database operations related to authorization."""

    @staticmethod
    def get_user_by_id(user_id, db_session=None):
        """Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: User details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor()

        # Check in users table
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            # Return user if found in users table
            return User(**user).to_dict()
        else:
            # Check in staff_users table if not found in users table
            cursor.execute("SELECT * FROM staff_users WHERE staff_id = ?", (user_id,))
            user = cursor.fetchone()
            return StaffUser(**user).to_dict() if user else None

    @staticmethod
    def get_user_by_username(username, db_session=None):
        """Retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            Object: User details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor()

        # Check in users table
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            # Return user if found in users table
            return User(**user)
        else:
            # Check in staff_users table if not found in users table
            cursor.execute("SELECT * FROM staff_users WHERE username = ?", (username,))
            user = cursor.fetchone()
            return StaffUser(**user) if user else None

    @staticmethod
    def create_user(data, db_session=None):
        """Create a new user in the database.

        Args:
            data (dict): Dictionary containing user details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created user.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO users (username, password_hash, email, created_at, updated_at, last_login, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            cursor.execute(statement, tuple(User(**data).to_dict().values())[1:])
        except DatabaseError:
            statement = """
                INSERT INTO staff_users (username, password_hash, name, email, phone, role, created_at, updated_at, last_login, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(statement, tuple(StaffUser(**data).to_dict().values())[1:])

        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_last_login(user_id, role=None, db_session=None):
        """Update the last login timestamp for a user.

        Args:
            user_id (int): The ID of the user to update.
            role: Optional role to differentiate between standard or staff/admin user.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor()

        if not role:
            statement = "UPDATE users SET last_login = ? WHERE user_id = ?"
        else:
            statement = "UPDATE staff_users SET last_login = ? WHERE user_id = ?"

        cursor.execute(statement, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
        db.commit()
        return cursor.rowcount