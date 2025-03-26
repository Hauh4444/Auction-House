from flask import jsonify, Response, session

from ..data_mappers import UserMapper, ProfileMapper
from flask_mail import Message
from flask import current_app as app
from flask_login import login_user
from flask import session
from flask_notifications import Notification
from ..data_mappers.user_login_mapper import UserMapper
from ..services.session_services import SessionService

class UserLoginService:
    @staticmethod
    def login_user(username, password):
        """
        Logs in a user by verifying their username and password.

        Args:
            username: The username of the user.
            password: The password provided by the user.

        Returns:
            A JSON response containing a success message and the user details if login is successful,
            or a 401 error if the username or password is incorrect.
        """
        user = UserMapper.get_user_by_username(username)
        if user and user.password_hash == UserLoginService.hash_password(password):
            UserMapper.update_last_login(user.user_id)  # Update the last login timestamp
            login_user(user, remember=True)  # Log User in using flask-login
            session["user_id"] = user.user_id  # Store user ID in session
            SessionService.create_session()

            # Send a login notification email
            UserLoginService.send_login_notification(user.email)

            # Send a login notification via Flask-Notifications
            notification = Notification('email_login', user=user)
            notifications.send(notification)

            return jsonify({"message": "Login successful", "user": user}), 200
        return jsonify({"error": "Invalid username or password"}), 401

    @staticmethod
    def send_login_notification(user_email):
        """Send a login notification email to the user."""
        msg = Message("Login Notification",
                      sender="your-email@gmail.com",  # Replace with your email
                      recipients=[user_email])
        msg.body = "You have successfully logged in to your account."

        # Send the email
        with app.app_context():
            mail.send(msg)

class UserService:
    @staticmethod
    def get_user(db_session=None):
        """
        Retrieves a user by their ID.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the user details if found, otherwise a 404 error with a message.
        """
        user = UserMapper.get_user(user_id=session.get("user_id"), db_session=db_session)

        if not user:
            response_data = {"error": "User not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "User found", "user": user}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def update_user(data, db_session=None):
        """
        Updates user information.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object indicating success or an error message if the user is not found.
        """
        updated_rows = UserMapper.update_user(user_id=session.get("user_id"), data=data, db_session=db_session)

        if not updated_rows:
            response_data = {"error": "User not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "User updated", "updated_rows": updated_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def delete_user(db_session=None):
        """
        Deletes a user by their ID.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with a success message if the user was deleted, or a 404 error if the user was not found.
        """
        deleted_rows = ProfileMapper.delete_profile(user_id=session.get("user_id"), db_session=db_session)

        if not deleted_rows:
            response_data = {"error": "Profile not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        deleted_rows = UserMapper.delete_user(user_id=session.get("user_id"), db_session=db_session)

        if not deleted_rows:
            response_data = {"error": "User not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "User and Profile deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

