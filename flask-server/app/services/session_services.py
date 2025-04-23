from flask import jsonify, session, Response

from datetime import datetime, timedelta

from ..data_mappers import SessionMapper


class SessionService:
    @staticmethod
    def create_session(db_session=None):
        """
        Creates a new user session.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object confirming session creation along with the session ID.
        """
        session_data = {
            "user_id": session.get("user_id"),
            "token": session.get("_id"),
            "role": session.get("role"),
            "expires_at": datetime.now() + timedelta(days=1),
        }
        session_id = SessionMapper.create_session(data=session_data, db_session=db_session)
        if not session_id:
            response_data = {"error": "Error creating session"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Session created", "session_id": session_id}
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")
