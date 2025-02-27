from ..database import get_db
from ..entities.session import Session


class SessionMapper:

    @staticmethod
    def get_all_sessions(session=None):
        """
        Retrieve all sessions from the database.

        Args:
            session: Optional database session to be used in tests.

        Returns:
            list: A list of session dictionaries retrieved from the database.
        """
        db = session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM sessions")
        sessions = cursor.fetchall()
        return [Session(**session).to_dict() for session in sessions]

    @staticmethod
    def get_session_by_id(session_id, session=None):
        """
        Retrieve a session by its ID from the database.

        Args:
            session_id (int): The ID of the session to retrieve.
            session: Optional database session to be used in tests.

        Returns:
            dict: A dictionary representation of the session if found, else None.
        """
        db = session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        session = cursor.fetchone()
        return Session(**session).to_dict() if session else None

    @staticmethod
    def create_session(data, session=None):
        """
        Create a new session in the database.

        Args:
            data (dict): The session data to be inserted into the database.
            session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created session.
        """
        db = session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO sessions 
            (user_id, token, created_at, expires_at) 
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Session(**data).to_dict().values())[1:])
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_session(session_id, data, session=None):
        """
        Update an existing session in the database.

        Args:
            session_id (int): The ID of the session to update.
            data (dict): The new data to update the session with.
            session: Optional database session to be used in tests.

        Returns:
            int: The number of rows affected by the update.
        """
        db = session or get_db()
        cursor = db.cursor()
        statement = """
            UPDATE sessions 
            SET user_id = ?, session_token = ?, created_at = ?, expires_at = ?
            WHERE session_id = ?
        """
        cursor.execute(statement, tuple(Session(**data).to_dict().values())[1:] + (session_id,))
        db.commit()
        return cursor.rowcount

    @staticmethod
    def delete_session(session_id, session=None):
        """
        Delete a session by its ID.

        Args:
            session_id (int): The ID of the session to delete.
            session: Optional database session to be used in tests.

        Returns:
            int: The number of rows deleted.
        """
        db = session or get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        db.commit()
        return cursor.rowcount
