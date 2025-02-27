from dataclasses import dataclass
from datetime import datetime


@dataclass
class Listing:
    """
    Represents a listing in the system.

    Attributes:
        listing_id (int, optional): The unique identifier for the listing.
        user_id (int): The ID of the user who created the listing.
        title (int): The title of the listing.
        title_short (str): A short version of the title.
        description (str): The detailed description of the listing.
        item_specifics (str): Specific details about the item.
        category_id (str): The category the listing belongs to.
        listing_type (str): The type of listing (e.g., auction, buy now).
        buy_now_price (float): The price to buy the item immediately.
        status (str): The status of the listing (e.g., active, sold, expired).
        image_encoded (str): Encoded image data of the listing.
        starting_price (float, optional): The starting price for auctions.
        reserve_price (float, optional): The minimum price a seller is willing to accept.
        current_price (float, optional): The current price in an auction.
        auction_start (datetime, optional): The start time of the auction.
        auction_end (datetime, optional): The end time of the auction.
        bids (int, optional): The number of bids placed.
        purchases (int, optional): The number of purchases made.
        average_review (float, optional): The average review score.
        total_reviews (int, optional): The total number of reviews.
        created_at (datetime, optional): The creation timestamp.
        updated_at (datetime, optional): The last updated timestamp.
    """
    def __init__(
            self,
            user_id: int,
            category_id: int,
            title: str,
            title_short: str,
            description: str,
            item_specifics: str,
            listing_type: str, # "auction", "buy_now"
            buy_now_price: float,
            status: str, # "active", "sold", "cancelled", "ended", "draft"
            image_encoded: str,
            starting_price: float | None = None,
            reserve_price: float | None = None,
            current_price: float | None = None,
            auction_start: datetime | None = None,
            auction_end: datetime | None = None,
            bids: int | None = None,
            purchases: int | None = None,
            average_review: float | None = None,
            total_reviews: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            listing_id: int | None = None
    ):
        self.VALID_LISTING_TYPES = {"auction", "buy_now"}
        self.VALID_STATUSES = {"active", "sold", "cancelled", "ended", "draft"}
        if listing_type not in self.VALID_LISTING_TYPES:
            raise ValueError(f"Listing type must be one of {self.VALID_LISTING_TYPES}, got '{listing_type}' instead")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}, got '{status}' instead")

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
        """Converts the listing object to a dictionary representation."""
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