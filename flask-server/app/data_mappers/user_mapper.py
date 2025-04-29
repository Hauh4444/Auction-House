from pymysql import cursors
from datetime import datetime

from ..database import get_db
from ..entities import User


class UserMapper:
    @staticmethod
    def get_user(user_id: int, db_session=None):
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
        return User(db_session=db_session, **user).to_dict() if db_session else User(**user).to_dict() if user else None


    @staticmethod
    def update_user(user_id: int, data: dict, db_session=None):
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
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    data[key] = datetime.strptime(value, '%a, %d %b %Y %H:%M:%S GMT')
                except ValueError:
                    pass
            if isinstance(value, datetime):
                data[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        set_clause = ", ".join([f"{key} = %s" for key in data if key not in ["user_id", "created_at", "updated_at", "last_login"]])
        values = [data.get(key) for key in data if key not in ["user_id", "created_at", "updated_at", "last_login"]]
        values.append(datetime.now())
        values.append(user_id)
        statement = f"UPDATE users SET {set_clause}, updated_at = %s WHERE user_id = %s"
        cursor.execute(statement, values)
        db.commit()
        return cursor.rowcount


    @staticmethod
    def delete_user(user_id: int, db_session=None):
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