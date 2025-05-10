from datetime import datetime, date


class Profile:
    """
    Represents a profile in the system.

    Attributes:
        profile_id (int, optional): The unique identifier for the profile.
        user_id (int): The ID of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        date_of_birth (str): The user's date of birth.
        phone_number (str): The user's phone number.
        address (str): The user's address.
        city (str): The city where the user resides.
        state (str): The state where the user resides.
        country (str): The country of the user.
        profile_picture (str, optional): The encoded profile picture.
        bio (str, optional): A short biography of the user.
        social_links (dict, optional): A dictionary of social media links.
        created_at (datetime, optional): The creation timestamp.
        updated_at (datetime, optional): The last updated timestamp.
    """
    def __init__(
            self,
            user_id: int,
            first_name: str,
            last_name: str | None = None,
            date_of_birth: date | None = None,
            phone_number: str | None = None,
            address: str | None = None,
            city: str | None = None,
            state: str | None = None,
            country: str | None = None,
            profile_picture: str | None = None,
            bio: str | None = None,
            social_links: dict | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            profile_id: int | None = None
    ):
        # Type checks for required attributes
        if not isinstance(user_id, int):
            raise TypeError(f"user_id must be a int, got {type(user_id).__name__}")
        if not isinstance(first_name, str):
            raise TypeError(f"first_name must be a str, got {type(first_name).__name__}")

        # Type checks for optional attributes
        if last_name is not None and not isinstance(last_name, str):
            raise TypeError(f"last_name must be a str or None, got {type(last_name).__name__}")
        if date_of_birth is not None and not isinstance(date_of_birth, date):
            raise TypeError(f"date_of_birth must be a date or None, got {type(date_of_birth).__name__}")
        if phone_number is not None and not isinstance(phone_number, str):
            raise TypeError(f"phone_number must be a str or None, got {type(phone_number).__name__}")
        if address is not None and not isinstance(address, str):
            raise TypeError(f"address must be a str or None, got {type(address).__name__}")
        if city is not None and not isinstance(city, str):
            raise TypeError(f"city must be a str or None, got {type(city).__name__}")
        if state is not None and not isinstance(state, str):
            raise TypeError(f"state must be a str or None, got {type(state).__name__}")
        if country is not None and not isinstance(country, str):
            raise TypeError(f"country must be a str or None, got {type(country).__name__}")
        if profile_picture is not None and not isinstance(profile_picture, str):
            raise TypeError(f"profile_picture must be a str or None, got {type(profile_picture).__name__}")
        if bio is not None and not isinstance(bio, str):
            raise TypeError(f"bio must be a str or None, got {type(bio).__name__}")
        if social_links is not None and not isinstance(social_links, dict):
            raise TypeError(f"social_links must be a dict or None, got {type(social_links).__name__}")
        if created_at is not None and not isinstance(created_at, (datetime, str)):
            raise TypeError(f"created_at must be a datetime or None, got {type(created_at).__name__}")
        if updated_at is not None and not isinstance(updated_at, (datetime, str)):
            raise TypeError(f"updated_at must be a datetime or None, got {type(updated_at).__name__}")
        if profile_id is not None and not isinstance(profile_id, int):
            raise TypeError(f"profile_id must be a int or None, got {type(profile_id).__name__}")

        self.profile_id = profile_id
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.profile_picture = profile_picture
        self.bio = bio
        self.social_links = social_links
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self):
        """Converts the profile object to a dictionary representation."""
        return {
            "profile_id": self.profile_id,
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "phone_number": self.phone_number,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "profile_picture": self.profile_picture,
            "bio": self.bio,
            "social_links": self.social_links,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
