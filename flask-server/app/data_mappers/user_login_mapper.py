from ..database import get_db
from ..entities.user import User
from ..entities.staff_user import StaffUser
from datetime import datetime


class UserMapper:
    """Handles database operations related to user logins."""

    @staticmethod
    def get_user_by_id(user_id, session=None):
        """Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.
            session: Optional database session to be used in tests.

        Returns:
            dict: User details if found, otherwise None.
        """
        db = session or get_db()
        cursor = db.cursor()

        # Check in users table
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            # Return user if found in users table
            return User(**user).to_dict()
        else:
            # Check in staff_users table if not found in users table
            cursor.execute("SELECT * FROM staff_users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            return StaffUser(**user).to_dict() if user else None

    @staticmethod
    def get_user_by_username(username, session=None):
        """Retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.
            session: Optional database session to be used in tests.

        Returns:
            Object: User details if found, otherwise None.
        """
        db = session or get_db()
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
    def create_user(data, session=None):
        """Create a new user in the database.

        Args:
            data (dict): Dictionary containing user details.
            session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created user.
        """
        db = session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO users (username, password_hash, email, created_at, updated_at, last_login, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(statement, (
            data["username"],
            data["password_hash"],
            data["email"],
            data.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            data.get("updated_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            data.get("last_login", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            data.get("is_active", True)
        ))
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_user(user_id, data, session=None):
        """Update an existing user.

        Args:
            user_id (int): The ID of the user to update.
            data (dict): Dictionary of fields to update.
            session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = session or get_db()
        cursor = db.cursor()
        conditions = [f"{key} = ?" for key in data.keys()]
        statement = f"UPDATE users SET {', '.join(conditions)} WHERE user_id = ?"
        cursor.execute(statement, tuple(data.values()) + (user_id,))
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_user(user_id, session=None):
        """Delete a user by their ID.

        Args:
            user_id (int): The ID of the user to delete.
            session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = session or get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        db.commit()
        return cursor.rowcount

    @staticmethod
    def update_last_login(user_id, session=None):
        """Update the last login timestamp for a user.

        Args:
            user_id (int): The ID of the user to update.
            session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = session or get_db()
        cursor = db.cursor()
        statement = "UPDATE users SET last_login = ? WHERE user_id = ?"
        cursor.execute(statement, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
        db.commit()
        return cursor.rowcount