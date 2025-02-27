from ..database import get_db
from ..entities.user import User


class UserMapper:
    """Handles database operations related to users."""

    @staticmethod
    def get_user(user_id, db_session=None):
        """Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: User details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        return User(**user).to_dict()

    @staticmethod
    def update_user(user_id, data, db_session=None):
        """Update an existing user.

        Args:
            user_id (int): The ID of the user to update.
            data (dict): Dictionary of fields to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        conditions = [f"{key} = ?" for key in data.keys()]
        statement = f"UPDATE users SET {', '.join(conditions)} WHERE user_id = ?"
        cursor.execute(statement, tuple(data.values()) + (user_id,))
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_user(user_id, db_session=None):
        """Delete a user by their ID.

        Args:
            user_id (int): The ID of the user to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        db.commit()
        return cursor.rowcount