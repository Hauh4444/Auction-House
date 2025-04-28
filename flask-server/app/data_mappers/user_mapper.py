from pymysql import cursors
from datetime import datetime

from ..database.connection import get_db
from ..entities import User


class UserMapper:
    @staticmethod
    def get_user(user_id, db_session=None):
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: User details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor)  # type: ignore
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            return None  # handle not found
        return User(db_session=db_session, **user).to_dict()  # <-- PASS db_session here


    @staticmethod
    def update_user(user_id, data, db_session=None):
        """
        Update an existing user.

        Args:
            user_id (int): The ID of the user to update.
            data (dict): Dictionary of fields to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        set_clause = ", ".join([f"{key} = %s" for key in data if key not in ["user_id", "updated_at"]])
        values = [data.get(key) for key in data if key not in ["user_id", "updated_at"]]
        values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        values.append(user_id)
        statement = f"UPDATE users SET {set_clause}, updated_at = %s WHERE user_id = %s"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_user(user_id, db_session=None):
        """
        Delete a user by their ID.

        Args:
            user_id (int): The ID of the user to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor(cursors.DictCursor) # type: ignore
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        db.commit()
        return cursor.rowcount