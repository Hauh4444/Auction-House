from ..database import get_db
from ..entities import Profile


class ProfileMapper:
    """Handles database operations related to profiles."""
    @staticmethod
    def get_all_profiles(db_session=None):
        """
        Retrieve all profiles from the database.

        Args:
            db_session: Optional database session to be used in tests.

        Returns:
            list: A list of profile dictionaries.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM profiles")
        profiles = cursor.fetchall()
        return [Profile(**profile).to_dict() for profile in profiles]


    @staticmethod
    def get_profile(user_id, db_session=None):
        """
        Retrieve a profile by its associated user ID.

        Args:
            user_id (int): The ID of the user to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: profile details if found, otherwise None.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
        profile = cursor.fetchone()
        return Profile(**profile).to_dict() if profile else None


    @staticmethod
    def create_profile(data, db_session=None):
        """Create a new profile in the database.

        Args:
            data (dict): Dictionary containing profile details.
            db_session: Optional database session to be used in tests.

        Returns:
            int: The ID of the newly created profile.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        statement = """
            INSERT INTO profiles 
            (user_id, first_name, last_name, date_of_birth, phone_number, address, city, state, country, profile_picture, bio, social_links, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(statement, tuple(Profile(**data).to_dict().values())[1:])
        db.commit()
        return cursor.lastrowid


    @staticmethod
    def update_profile(profile_id, data, db_session=None):
        """Update an existing profile.

        Args:
            profile_id (int): The ID of the profile to update.
            data (dict): Dictionary of fields to update.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows updated.
        """
        db = db_session or get_db()
        cursor = db.cursor()

        # Filter out the keys you don't want to update
        filtered_data = {key: value for key, value in data.items() if key not in ["profile_id", "created_at"]}

        # Build the condition placeholders (SET part)
        conditions = [f"{key} = ?" for key in filtered_data]
        statement = "UPDATE profiles SET " + ", ".join(conditions) + " WHERE profile_id = ?"

        # Create the values list (filtered data values + profile_id for WHERE clause)
        values = list(filtered_data.values()) + [profile_id]

        # Execute the statement
        cursor.execute(statement, values)
        db.commit()

        # Return the number of rows affected
        return cursor.rowcount


    @staticmethod
    def delete_profile(user_id, db_session=None):
        """Delete a profile by its ID.

        Args:
            user_id (int): The ID of the user associated with the profile to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            int: Number of rows deleted.
        """
        db = db_session or get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM profiles WHERE user_id = ?", (user_id,))
        db.commit()
        return cursor.rowcount
