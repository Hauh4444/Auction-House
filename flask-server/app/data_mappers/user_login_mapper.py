from ..database import get_db
from ..entities.user import User
from datetime import datetime


class UserMapper:
    """Handles database operations related to user logins."""

    @staticmethod
    def get_user_by_id(user_id):
        """Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            dict: User details if found, otherwise None.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        return User(**user).to_dict() if user else None

    @staticmethod
    def get_user_by_username(username):
        """Retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            Object: User details if found, otherwise None.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        return User(**user) if user else None

    @staticmethod
    def update_last_login(user_id):
        """Update the last login timestamp for a user.

        Args:
            user_id (int): The ID of the user to update.

        Returns:
            int: Number of rows updated.
        """
        db = get_db()
        cursor = db.cursor()
        statement = "UPDATE users SET last_login = ? WHERE user_id = ?"
        cursor.execute(statement, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
        db.commit()
        return cursor.rowcount

    @staticmethod
    def create_user(data):
        """Create a new user in the database.

        Args:
            data (dict): Dictionary containing user details.

        Returns:
            int: The ID of the newly created user.
        """
        db = get_db()
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
    def update_user(user_id, data):
        """Update an existing user.

        Args:
            user_id (int): The ID of the user to update.
            data (dict): Dictionary of fields to update.

        Returns:
            int: Number of rows updated.
        """
        db = get_db()
        cursor = db.cursor()
        conditions = [f"{key} = ?" for key in data.keys()]
        statement = f"UPDATE users SET {', '.join(conditions)} WHERE user_id = ?"
        cursor.execute(statement, tuple(data.values()) + (user_id,))
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_user(user_id):
        """Delete a user by their ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            int: Number of rows deleted.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        db.commit()
        return cursor.rowcount
