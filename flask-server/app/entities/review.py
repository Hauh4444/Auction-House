from datetime import datetime


class Review:
    """
    Represents a review in the system.

    Attributes:
        review_id (int, optional): The unique identifier for the review.
        listing_id (int): The ID of the listing being reviewed.
        user_id (int): The ID of the user who left the review.
        username (str): The username of the reviewer.
        title (str): The title of the review.
        description (str): The detailed review text.
        stars (float): The rating given in the review.
        created_at (datetime, optional): The timestamp when the review was created.
    """
    def __init__(
            self,
            listing_id: int,
            user_id: int,
            username: str,
            title: str,
            description: str,
            stars: float,
            created_at: datetime | None = None,
            review_id: int | None = None
    ):
        self.review_id = review_id
        self.listing_id = listing_id
        self.user_id = user_id
        self.username = username
        self.title = title
        self.description = description
        self.stars = stars
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        """Converts the review object to a dictionary representation."""
        return {
            "review_id": self.review_id,
            "listing_id": self.listing_id,
            "user_id": self.user_id,
            "username": self.username,
            "title": self.title,
            "description": self.description,
            "stars": self.stars,
            "created_at": self.created_at
        }
