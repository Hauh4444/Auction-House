from dataclasses import dataclass
from datetime import datetime


@dataclass
class Listing:
    """Represents a listing in the auction system."""

    def __init__(
            self,
            user_id: int,  # ID of the user creating the listing
            title: str,  # Full title of the listing
            title_short: str,  # Shortened title for display
            description: str,  # Detailed description of the listing
            item_specifics: str,  # Specific attributes of the item
            category_id: str,  # ID of the category to which the listing belongs
            listing_type: str,  # Type of listing (e.g., auction, fixed price)
            buy_now_price: float,  # Price for a "Buy Now" option
            status: str,  # Current status of the listing (e.g., active, sold)
            image_encoded: str,  # Base64-encoded image for the listing
            starting_price: float | None = None,  # Starting price for the listing
            reserve_price: float | None = None,  # Reserve price (if any)
            current_price: float | None = None,  # Current price of the listing
            auction_start: datetime | None = None,  # Start date for auction
            auction_end: datetime | None = None,  # End date for auction
            bids: int | None = None,  # Number of bids received
            purchases: int | None = None,  # Number of times the listing has been purchased
            average_review: float | None = None,  # Average rating of the listing
            total_reviews: int | None = None,  # Total number of reviews
            created_at: datetime | None = None,  # Timestamp of creation
            updated_at: datetime | None = None,  # Timestamp of last update
            listing_id: int | None = None  # ID of the listing
    ):
        self.listing_id = listing_id
        self.user_id = user_id
        self.title = title
        self.title_short = title_short
        self.description = description
        self.item_specifics = item_specifics
        self.category_id = category_id
        self.listing_type = listing_type
        self.starting_price = starting_price
        self.reserve_price = reserve_price
        self.current_price = current_price
        self.buy_now_price = buy_now_price
        self.auction_start = auction_start
        self.auction_end = auction_end
        self.status = status
        self.image_encoded = image_encoded
        self.bids = bids
        self.purchases = purchases
        self.average_review = average_review
        self.total_reviews = total_reviews
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Convert the listing to a dictionary format for serialization."""
        return {
            "listing_id": self.listing_id,
            "user_id": self.user_id,
            "title": self.title,
            "title_short": self.title_short,
            "description": self.description,
            "item_specifics": self.item_specifics,
            "category_id": self.category_id,
            "listing_type": self.listing_type,
            "starting_price": self.starting_price,
            "reserve_price": self.reserve_price,
            "current_price": self.current_price,
            "buy_now_price": self.buy_now_price,
            "auction_start": self.auction_start,
            "auction_end": self.auction_end,
            "status": self.status,
            "image_encoded": self.image_encoded,
            "bids": self.bids,
            "purchases": self.purchases,
            "average_review": self.average_review,
            "total_reviews": self.total_reviews,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


@dataclass
class Category:
    """Represents a category in the auction system."""

    def __init__(
            self,
            name: str,  # Name of the category
            description: str,  # Description of the category
            image_encoded: str | None = None,  # Optional base64-encoded image for the category
            created_at: datetime | None = None,  # Timestamp of category creation
            updated_at: datetime | None = None,  # Timestamp of last category update
            category_id: int | None = None  # ID of the category
    ):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.image_encoded = image_encoded
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Convert the category to a dictionary format for serialization."""
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "image_encoded": self.image_encoded,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
