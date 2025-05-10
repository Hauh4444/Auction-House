from datetime import datetime


class Listing:
    """
    Represents a listing in the system.

    Attributes:
        listing_id (int | None): The unique identifier for the listing.
        user_id (int): The identifier of the user who created the listing.
        category_id (int): The identifier of the category the listing belongs to.
        title (str): The full title of the listing.
        title_short (str): A shortened version of the title for display purposes.
        description (str): A detailed description of the item being listed.
        item_specifics (str): Specific details about the item (e.g., brand, condition).
        listing_type (str): The type of listing ("auction" or "buy_now").
        buy_now_price (float): The price at which the item can be bought immediately (for "buy_now" listings).
        starting_price (float | None): The starting price for auction listings (optional).
        reserve_price (float | None): The reserve price for auction listings (optional).
        current_price (float | None): The current price of the item (for auctions).
        auction_start (datetime | None): The start date and time of the auction (optional).
        auction_end (datetime | None): The end date and time of the auction (optional).
        status (str): The status of the listing ("active", "sold", "cancelled", "ended", "draft").
        image_encoded (str): The encoded image of the item for the listing.
        bids (int | None): The number of bids received (for auction listings, optional).
        purchases (int | None): The number of purchases made (for "buy_now" listings, optional).
        average_review (float | None): The average review rating of the listing (optional).
        total_reviews (int | None): The total number of reviews for the listing (optional).
        created_at (datetime | None): The date and time the listing was created.
        updated_at (datetime | None): The date and time the listing was last updated.
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
            buy_now_price: float | int,
            status: str, # "active", "sold", "cancelled", "ended", "draft"
            image_encoded: str,
            starting_price: float | int | None = None,
            reserve_price: float | int | None = None,
            current_price: float | int | None = None,
            auction_start: datetime | None = None,
            auction_end: datetime | None = None,
            bids: int | None = None,
            purchases: int | None = 0,
            average_review: float | int | None = None,
            total_reviews: int | None = 0,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
            listing_id: int | None = None
    ):
        self.VALID_LISTING_TYPES = {"auction", "buy_now"}
        self.VALID_STATUSES = {"active", "sold", "cancelled", "ended", "draft"}

        # Type checks for required attributes
        if not isinstance(user_id, int):
            raise TypeError(f"user_id must be an int, got {type(user_id).__name__}")
        if not isinstance(category_id, int):
            raise TypeError(f"category_id must be an int, got {type(category_id).__name__}")
        if not isinstance(title, str):
            raise TypeError(f"title must be a str, got {type(title).__name__}")
        if not isinstance(title_short, str):
            raise TypeError(f"title_short must be a str, got {type(title_short).__name__}")
        if not isinstance(description, str):
            raise TypeError(f"description must be a str, got {type(description).__name__}")
        if not isinstance(item_specifics, str):
            raise TypeError(f"item_specifics must be a str, got {type(item_specifics).__name__}")
        if not isinstance(listing_type, str):
            raise TypeError(f"listing_type must be a str, got {type(listing_type).__name__}")
        if not isinstance(buy_now_price, (float, int)):
            raise TypeError(f"buy_now_price must be a number, got {type(buy_now_price).__name__}")
        if not isinstance(status, str):
            raise TypeError(f"status must be a str, got {type(status).__name__}")
        if not isinstance(image_encoded, str):
            raise TypeError(f"image_encoded must be a str, got {type(image_encoded).__name__}")

        # Type checks for optional attributes
        if starting_price is not None and not isinstance(starting_price, (float, int)):
            raise TypeError(f"starting_price must be a number, got {type(starting_price).__name__}")
        if reserve_price is not None and not isinstance(reserve_price, (float, int)):
            raise TypeError(f"reserve_price must be a number, got {type(reserve_price).__name__}")
        if current_price is not None and not isinstance(current_price, (float, int)):
            raise TypeError(f"current_price must be a number, got {type(current_price).__name__}")
        if auction_start is not None and not isinstance(auction_start, (datetime, str)):
            raise TypeError(f"auction_start must be a datetime, str, or None, got {type(auction_start).__name__}")
        if auction_end is not None and not isinstance(auction_end, (datetime, str)):
            raise TypeError(f"auction_end must be a datetime, str, or None, got {type(auction_end).__name__}")
        if bids is not None and not isinstance(bids, int):
            raise TypeError(f"bids must be an int, got {type(bids).__name__}")
        if purchases is not None and not isinstance(purchases, int):
            raise TypeError(f"purchases must be an int, got {type(purchases).__name__}")
        if average_review is not None and not isinstance(average_review, (float, int)):
            raise TypeError(f"average_review must be a number, got {type(average_review).__name__}")
        if total_reviews is not None and not isinstance(total_reviews, int):
            raise TypeError(f"total_reviews must be an int, got {type(total_reviews).__name__}")
        if created_at is not None and not isinstance(created_at, (datetime, str)):
            raise TypeError(f"created_at must be a datetime, str, or None, got {type(created_at).__name__}")
        if updated_at is not None and not isinstance(updated_at, (datetime, str)):
            raise TypeError(f"updated_at must be a datetime, str, or None, got {type(updated_at).__name__}")

        # Value checks for enumerated attributes
        if listing_type not in self.VALID_LISTING_TYPES:
            raise ValueError(f"listing_type must be one of {self.VALID_LISTING_TYPES}, got '{listing_type}' instead")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"status must be one of {self.VALID_STATUSES}, got '{status}' instead")

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
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

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
