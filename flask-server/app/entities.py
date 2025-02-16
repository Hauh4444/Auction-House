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


@dataclass
class Category:
    """
    Represents a category in the system.

    Attributes:
        category_id (int, optional): The unique identifier for the category.
        name (str): The name of the category.
        description (str): The description of the category.
        image_encoded (str, optional): Encoded image data for the category.
        created_at (datetime, optional): The creation timestamp.
        updated_at (datetime, optional): The last updated timestamp.
    """
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
        """Converts the category object to a dictionary representation."""
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
    """
    Represents a transaction in the system.

    Attributes:
        transaction_id (int, optional): The unique identifier for the transaction.
        listing_id (int): The ID of the listing involved.
        buyer_id (int): The ID of the buyer.
        seller_id (int): The ID of the seller.
        transaction_date (datetime): The date and time of the transaction.
        transaction_type (str): The type of transaction ("auction" or "buy_now").
        amount (float): The transaction amount.
        payment_method (str): The method used for payment.
        status (str): The status of the transaction (e.g., pending, completed, canceled).
        shipping_address (str): The shipping address for the order.
        tracking_number (str, optional): The tracking number for shipment.
        created_at (datetime, optional): The creation timestamp.
        updated_at (datetime, optional): The last updated timestamp.
    """
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
        """Converts the transaction object to a dictionary representation."""
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
    """
    Represents an order in the system.

    Attributes:
        order_id (int, optional): The unique identifier for the order.
        user_id (int): The ID of the user who placed the order.
        order_date (datetime): The date and time the order was placed.
        status (str): The status of the order (e.g., processing, shipped, delivered).
        total_amount (float): The total amount of the order.
        payment_status (str): The payment status (e.g., paid, pending, failed).
        payment_method (str): The method used for payment.
        shipping_address (str): The shipping address.
        shipping_method (str): The chosen shipping method.
        tracking_number (str, optional): The tracking number for shipment.
        shipping_cost (float, optional): The cost of shipping.
        created_at (datetime, optional): The creation timestamp.
        updated_at (datetime, optional): The last updated timestamp.
    """
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

    def to_dict(self):
        """Converts the order object to a dictionary representation."""
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "order_date": self.order_date,
            "status": self.status,
            "total_amount": self.total_amount,
            "payment_status": self.payment_status,
            "payement_method": self.payment_method,
            "shipping_address": self.shipping_address,
            "shipping_method": self.shipping_method,
            "tracking_number": self.tracking_number,
            "shipping_cost": self.shipping_cost,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


@dataclass
class UserProfile:
    """
    Represents a user profile in the system.

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
        """Converts the user profile object to a dictionary representation."""
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
