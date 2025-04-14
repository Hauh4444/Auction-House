from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from datetime import datetime
from app.models import User  # Assuming a SQLAlchemy-based User model
from app.database import db_session  # Assuming a SQLAlchemy session

class AuthService:

    @staticmethod
    def check_auth_status():
        """
        Check the authentication status of the current user.

        Returns:
            Response: A JSON response indicating whether the user is logged in or not.
        """
        if current_user.is_authenticated:
            return jsonify({"authenticated": True, "user": current_user.username})
        return jsonify({"authenticated": False})

    @staticmethod
    def create_user(data, db_session=db_session):
        """
        Register a new user.
        Args:
            data (dict): The user details.
        Returns:
            Response: A JSON response indicating the registration status.
        """
        # Validate the data (basic validation for required fields)
        if not data.get("username") or not data.get("password") or not data.get("email"):
            return jsonify({"error": "Username, password, and email are required"}), 400
        
        # Hash the password
        hashed_password = generate_password_hash(data["password"])

        # Create and store the new user
        new_user = User(
            username=data["username"],
            password_hash=hashed_password,
            email=data["email"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            last_login=None,
            is_active=True
        )
        
        db_session.add(new_user)
        db_session.commit()

        return jsonify({"message": "User created successfully", "user_id": new_user.id}), 201

    @staticmethod
    def login(data, db_session=db_session):
        """
        Login a user by verifying their username and password.
        Args:
            data (dict): The user's username and password.
        Returns:
            Response: A JSON response indicating the login status.
        """
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        user = db_session.query(User).filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid username or password"}), 401

        # Log in the user
        login_user(user)

        return jsonify({"message": "Login successful", "user_id": user.id}), 200

    @staticmethod
    def logout():
        """
        Log out the current user.
        This will invalidate the session or token.
        Returns:
            Response: A JSON response indicating the logout status.
        """
        logout_user()
        return jsonify({"message": "Logged out successfully"}), 200

    @staticmethod
    def password_reset_request(db_session=db_session):
        """
        Request a password reset email.
        Args:
            db_session (Session): Database session.
        Returns:
            Response: A JSON response indicating the status of the reset request.
        """
        # Implement actual password reset request logic (e.g., send email with token)
        # Here, just a mock response for now
        return jsonify({"message": "Password reset request received, check your email for instructions."}), 200

    @staticmethod
    def reset_user_password(reset_token, new_password, db_session=db_session):
        """
        Reset the user password.
        Args:
            reset_token (str): Token to verify the reset request.
            new_password (str): The new password to set.
        Returns:
            Response: A JSON response indicating the status of the password reset.
        """
        # Logic to validate the token and reset the password
        if not reset_token or not new_password:
            return jsonify({"error": "Reset token and new password are required"}), 400

        # Example: Fetch user by reset token (Here, assuming token validation is skipped)
        user = db_session.query(User).filter_by(reset_token=reset_token).first()

        if not user:
            return jsonify({"error": "Invalid reset token"}), 400

        # Hash the new password and update
        user.password_hash = generate_password_hash(new_password)
        db_session.commit()

        return jsonify({"message": "Password successfully reset."}), 200
