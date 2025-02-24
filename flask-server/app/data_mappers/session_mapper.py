from ..database import get_db
from ..entities.session import Session

class SessionMapper:
    
    @staticmethod
    def get_all_sessions():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM sessions")
        sessions = cursor.fetchall()
        return [Session(**session).to_dict() for session in sessions]

    @staticmethod
    def get_session_by_id(session_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        session = cursor.fetchone()
        return Session(**session).to_dict() if session else None
    
    @staticmethod
    def create_session(data):
        db = get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO sessions 
            (user_id, session_token, created_at, expires_at) 
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Session(**data).to_dict().values())[1:])
        db.commit()
        return cursor.lastrowid
    
    @staticmethod
    def update_session(session_id, data):
        db = get_db()
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
    def delete_session(session_id):
        """Delete a session by its ID.
        
        Args:
            session_id (int): The ID of the session to delete.

        Returns:
            int: Number of rows deleted.    
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        db.commit()
        return cursor.rowcount