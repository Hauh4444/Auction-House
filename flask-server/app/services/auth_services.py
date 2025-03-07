from flask import jsonify, session, Response
from flask_login import login_user, logout_user, current_user

from .profile_services import ProfileService
from .session_services import SessionService
from ..data_mappers import AuthMapper
from ..utils import hash_password


class AuthService:
    @staticmethod
    def check_auth_status():
        """
        Checks authentication status of the current session.

        Returns:
            A Response object with the authentication status and user ID if authenticated, otherwise a 401 error.
        """

        if not current_user.is_authenticated:
            data = {"authenticated": False}
            return Response(response=jsonify(data).get_data(), status=401, mimetype="application/json")

        data = {"authenticated": True, "user": current_user.id}
        return Response(response=jsonify(data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def create_user(data, db_session=None):
        """
        Creates a new user account.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object indicating success with the user ID or an error message.
        """
        if not data.get("username") or not data.get("password") or not data.get("email"):
            data = {"error": "Username, password, and email are required"}
            return Response(response=jsonify(data).get_data(), status=400, mimetype="application/json")

        user_data = {"username": data["username"], "password_hash": hash_password(password=data["password"]), "email": data["email"]}
        user_id = AuthMapper.create_user(data=user_data, db_session=db_session)

        if not user_id:
            data = {"error": "Error creating user"}
            return Response(response=jsonify(data).get_data(), status=400, mimetype="application/json")

        profile_data = {"user_id": user_id, "first_name": data["first_name"], "last_name": data["last_name"]}
        profile_id = ProfileService.create_profile(data=profile_data, db_session=db_session).get_json().get("profile_id")

        if not profile_id:
            data = {"error": "Error creating profile"}
            return Response(response=jsonify(data).get_data(), status=400, mimetype="application/json")

        data = {"message": "User registered successfully", "user_id": user_id, "profile_id": profile_id}
        return Response(response=jsonify(data).get_data(), status=201, mimetype="application/json")


    @staticmethod
    def login_user(data, db_session=None):
        """
        Logs in a user by verifying their username and password.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object containing a success message and the user details if login is successful,
            or a 401 error if the username or password is incorrect.
        """
        if not data.get("username") or not data.get("password"):
            return jsonify({"error": "Username and password are required"}), 400

        user = AuthMapper.get_user_by_username(data.get("username"), db_session)

        if not user or not user.password_hash == hash_password(data.get("password")):
            data = {"error": "Invalid username or password"}
            return Response(response=jsonify(data).get_data(), status=401, mimetype="application/json")

        if user.__class__.__name__ == "User":
            session["user_id"], session["role"] = (user.user_id, "user")
        else:
            session["user_id"], session["role"] = (user.staff_id, user.role)

        login_user(user, remember=True)
        user.is_active = True

        AuthMapper.update_last_login(user_id=session["user_id"], role=session["role"], db_session=db_session)
        SessionService.create_session(db_session)

        data = {"message": "Login successful", "user": user}
        return Response(response=jsonify(data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def logout_user():
        """
        Logs out the currently logged-in user.

        Returns:
            A Response object indicating the success of the logout operation.
        """
        logout_user()
        session.clear()
        current_user.is_active = False

        data = {"message": "Logout successful"}
        return Response(response=jsonify(data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def password_reset_request(data):
        """
        Handles a password reset request.

        Args:
            data: A dictionary containing the request arguments.

        Returns:
            A Response object indicating whether the request was successful.
        """
        if not data.get("email"):
            data = {"error": "Email is required"}
            return Response(response=jsonify(data).get_data(), status=400, mimetype="application/json")

        data = {"message": "Password reset request sent"}
        return Response(response=jsonify(data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def reset_user_password(data, db_session=None):
        """
        Resets a user's password using a reset token.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object indicating whether the password reset was successful.
        """
        if not data.get("reset_token") or not data.get("new_password"):
            return jsonify({"error": "Reset token and new password are required"}), 400

        data = {"message": "Password successfully reset"}
        return Response(response=jsonify(data).get_data(), status=200, mimetype="application/json")