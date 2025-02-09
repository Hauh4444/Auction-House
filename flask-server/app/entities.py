from dataclasses import dataclass
from datetime import datetime

@dataclass
class Listing:
    def __init__(
        self,
        listing_id: int,
        user_id: int,
        title: int,
        title_short: str,
        description: str,
        category_id: str,
        listing_type: str,
        starting_price: float,
        reserve_price: float,
        current_price: float,
        buy_now_price: float,
        auction_start: datetime,
        auction_end: datetime,
        status: str,
        image_encoded: str,
        bids: int,
        purchases: int,
        average_review: float,
        total_reviews: int,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.listing_id = listing_id
        self.user_id = user_id
        self.title = title
        self.title_short = title_short
        self.description = description
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
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "listing_id": self.listing_id,
            "user_id": self.user_id,
            "title": self.title,
            "title_short": self.title_short,
            "description": self.description,
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
    def __init__(
        self,
        category_id: int,
        name: str,
        description: str,
        image_encoded: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.category_id = category_id
        self.name = name 
        self.description = description
        self.image_encoded = image_encoded
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "image_encoded": self.image_encoded,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }