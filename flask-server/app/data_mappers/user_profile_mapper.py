from ..database import get_db
from ..entities.user_profile import UserProfile


class UserProfileMapper:
    """Handles database operations related to user profiles."""

    @staticmethod
    def get_all_user_profiles():
        """Retrieve all user profiles from the database.

        Returns:
            list: A list of user profile dictionaries.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user_profiles")
        profiles = cursor.fetchall()
        return [UserProfile(**profile).to_dict() for profile in profiles]

    @staticmethod
    def get_user_profile(user_id):
        """Retrieve a user profile by its associated user ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            dict: User profile details if found, otherwise None.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
        profile = cursor.fetchone()
        return UserProfile(**profile).to_dict() if profile else None

    @staticmethod
    def create_user_profile(data):
        """Create a new user profile in the database.

        Args:
            data (dict): Dictionary containing profile details.

        Returns:
            int: The ID of the newly created profile.
        """
        db = get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO user_profiles 
            (user_id, first_name, last_name, date_of_birth, phone_number, address, city, state, country, profile_picture, bio, social_links, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(UserProfile(**data).to_dict().values())[1:])
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def update_user_profile(profile_id, data):
        """Update an existing user profile.

        Args:
            profile_id (int): The ID of the profile to update.
            data (dict): Dictionary of fields to update.

        Returns:
            int: Number of rows updated.
        """
        db = get_db()
        cursor = db.cursor()

        # Filter out the keys you don't want to update
        filtered_data = {key: value for key, value in data.items() if key not in ["profile_id", "created_at"]}

        # Build the condition placeholders (SET part)
        conditions = [f"{key} = ?" for key in filtered_data]
        statement = "UPDATE user_profiles SET " + ", ".join(conditions) + " WHERE profile_id = ?"

        # Create the values list (filtered data values + profile_id for WHERE clause)
        values = list(filtered_data.values()) + [profile_id]

        # Execute the statement
        cursor.execute(statement, values)
        db.commit()

        # Return the number of rows affected
        return cursor.rowcount

    @staticmethod
    def delete_user_profile(user_id):
        """Delete a user profile by its ID.

        Args:
            user_id (int): The ID of the user associated with the profile to delete.

        Returns:
            int: Number of rows deleted.
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM user_profiles WHERE user_id = ?", (user_id,))
        db.commit()
        return cursor.rowcount
