from dataclasses import dataclass
from datetime import datetime

@dataclass
class Listing:
    def __init__(
        self,
        user_id: int,
        title: int,
        title_short: str,
        description: str,
        item_specifics: str,
        category_id: str,
        listing_type: str,
        buy_now_price: float,
        status: str,
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
    def __init__(
        self,
        name: str,
        description: str,
        image_encoded: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        category_id: int | None = None
    ):
        self.category_id = category_id
        self.name = name 
        self.description = description
        self.image_encoded = image_encoded
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "image_encoded": self.image_encoded,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
@dataclass
class Transaction:
    def __init__(
        self,
        listing_id: int,
        buyer_id: int,
        seller_id: int,
        transaction_date: datetime,
        transaction_type: str,  # "auction" or "buy_now"
        amount: float,
        payment_method: str,
        status: str,  # e.g., "pending", "completed", "canceled"
        shipping_address: str,
        tracking_number: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        transaction_id: int | None = None
    ):
        self.transaction_id = transaction_id
        self.listing_id = listing_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.transaction_date = transaction_date.strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_type = transaction_type
        self.amount = amount
        self.payment_method = payment_method
        self.status = status
        self.shipping_address = shipping_address
        self.tracking_number = tracking_number
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "listing_id": self.listing_id,
            "buyer_id": self.buyer_id,
            "seller_id": self.seller_id,
            "transaction_date": self.transaction_date,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "status": self.status,
            "shipping_address": self.shipping_address,
            "tracking_number": self.tracking_number,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
@dataclass
class Order:
    def __init__(
        self,
        user_id: int,
        order_date: datetime,
        status: str,
        total_amount: float,
        payment_status: str,
        payment_method: str,
        shipping_address: str,
        shipping_method: str,
        tracking_number: str | None = None,
        shipping_cost: float | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        order_id: int | None = None
    ):
        self.order_id = order_id
        self.user_id = user_id
        self.order_date = order_date.strftime("%Y-%m-%d %H:%M:%S")
        self.status = status
        self.total_amount = total_amount
        self.payment_status = payment_status
        self.payment_method = payment_method
        self.shipping_address = shipping_address
        self.shipping_method = shipping_method
        self.tracking_number = tracking_number
        self.shipping_cost = shipping_cost
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@dataclass
class UserProfile:
    def __init__(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        phone_number: str,
        address: str,
        city: str,
        state: str,
        country: str,
        profile_picture: str | None = None,
        bio: str | None = None,
        social_links: dict | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        profile_id: int | None = None
    ):
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
        self.social_links = social_links or {}
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
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
