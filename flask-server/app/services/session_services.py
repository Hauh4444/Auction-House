from flask import jsonify, session

from datetime import datetime, timedelta

from ..data_mappers.session_mapper import SessionMapper

class SessionService:
    @staticmethod
    def create_session():
        # Set data from session information
        data = {
            "user_id": session["user_id"],
            "session_token": session["token"],
            "expires_at": datetime.now() + timedelta(days=1),
        }
        session_id = SessionMapper.create_session(data)
        return jsonify({"message": "Session created", "session_id": session_id}), 201