from app.database import db
from app.entities.listing import Listing
from app.entities.transaction import Transaction

class PurchaseService:
    @staticmethod
    def process_purchase(listing_id, user_id):
        listing = Listing.query.get(listing_id)
        if not listing:
            return {"error": "Listing not found"}, 404

        if listing.status != 'available':
            return {"error": "Listing is not available for purchase"}, 400

        # Update listing status
        listing.status = 'sold'
        db.session.commit()

        # Record the transaction
        transaction = Transaction(
            listing_id=listing_id,
            buyer_id=user_id,
            price=listing.buy_now_price,
            status='completed'
        )
        db.session.add(transaction)
        db.session.commit()

        return {"message": "Purchase successful"}, 200