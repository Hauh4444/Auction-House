from datetime import datetime
from app.database import db
from app.entities.listing import Listing
from app.entities.transaction import Transaction
from app.services.profile_services import ProfileService

class PurchaseService:
    @staticmethod
    def process_purchase(listing_id, user_id):
        listing = Listing.query.get(listing_id)
        if not listing:
            return {"error": "Listing not found"}, 404

        if listing.status != 'active':
            return {"error": "Listing is not available for purchase"}, 400

        # Retrieve the user's profile
        profile_response = ProfileService.get_profile(user_id=user_id)
        if profile_response.status_code != 200:
            return {"error": "User profile not found"}, 404

        profile = profile_response.json['profile']

        # Construct the shipping address
        shipping_address = f"{profile['address']}, {profile['city']}, {profile['state']}, {profile['country']}"

        # Update listing status
        listing.status = 'sold'
        db.session.commit()

        # Record the transaction
        transaction = Transaction(
            listing_id=listing_id,
            buyer_id=user_id,
            seller_id=listing.user_id,  
            transaction_date=datetime.now(),
            transaction_type=listing.listing_type,
            amount=listing.buy_now_price if listing.listing_type == 'buy_now' else listing.current_price,
            payment_method='credit_card',  # Default to credit card
            status='completed',
            shipping_address=shipping_address,
            tracking_number=None
        )
        db.session.add(transaction)
        db.session.commit()

        return {"message": "Purchase successful"}, 200