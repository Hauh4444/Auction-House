from flask import jsonify, session

from datetime import datetime, timedelta

from ..data_mappers.session_mapper import SessionMapper

class SessionService:
    @staticmethod
    def create_session():
        """
        Creates a new user session.

        Returns:
            A JSON response confirming session creation along with the session ID.
        """
        data = {
            "user_id": session["user_id"],
            "token": session["_id"],
            "expires_at": datetime.now() + timedelta(days=1),
        }
        session_id = SessionMapper.create_session(data)
        return jsonify({"message": "Session created", "session_id": session_id}), 201