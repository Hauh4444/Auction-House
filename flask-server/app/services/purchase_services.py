from flask import Response, jsonify
from flask_login import current_user

from datetime import date, datetime, timedelta
from dotenv import load_dotenv
import stripe, os

from ..services import ProfileService
from ..data_mappers import OrderMapper, TransactionMapper, DeliveryMapper, ListingMapper

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class PurchaseService:
    """For now, we mock most of the external data due to integration unavailability."""
    @staticmethod
    def process_purchase(data, db_session=None):
        """
        Process Purchase Request

        Args:
            data (dict): The purchase data containing listings and total_amount.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response with an error message on failure or the result of order creation.
        """
        user_id, listings, total_amount = current_user.id, data.get('listings'), data.get("total_amount")
        if not listings or not total_amount:
            response_data = {"error": "Required data not provided"}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        # Retrieve the user's profile
        profile = ProfileService.get_profile(db_session=db_session).json.get("profile")
        if not profile:
            response_data = {"error": "Profile not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        data = {
            "user_id": user_id,
            "listings": listings,
            "total_amount": total_amount,
            "profile": profile,
        }
        return PurchaseService.create_order(data=data, db_session=db_session)
    
    @staticmethod
    def process_payment(data, db_session=None):
        try:
            amount = int(float(data.get("amount")) * 100)
            currency = data.get("currency")
            success_url = data.get("success_url")
            cancel_url = data.get("cancel_url")

            if amount <= 0:
                return Response(response=jsonify({"error": "Invalid amount"}).get_data(), status=400, mimetype="application/json")

            session = stripe.checkout.Session.create(
                payment_method_types = ["card"],
                line_items = [{
                    "price_data": {
                        "currency": currency,
                        "product_data": {
                            "name": "Purchase from Marketplace",
                        },
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }],
                mode = "payment",
                success_url = success_url,
                cancel_url = cancel_url,
            )

            response_data = {"message": "Stripe session created", "id": session.id}
            return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

        except stripe.error.StripeError as e:
            response_data = {"error": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
        except Exception as e:
            response_data = {"error": "Internal server error", "details": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=500, mimetype="application/json")


    @staticmethod
    def create_order(data, db_session=None):
        """
        Create Order

        Args:
            data (dict): Purchase data including user_id, listings, total_amount, and profile.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response with an error message if order creation fails, or the result of transaction creation.
        """
        order_data = {
            "user_id": data.get("user_id"),
            "order_date": datetime.now(),
            "status": "processing",
        }
        order_id = OrderMapper.create_order(data=order_data, db_session=db_session)
        if not order_id:
            response_data = {"error": "Error creating order"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        data.update(order_id=order_id)
        return PurchaseService.create_transaction(data=data, db_session=db_session)


    @staticmethod
    def create_transaction(data, db_session=None):
        """
        Create Transaction

        Args:
            data (dict): Purchase data including order_id, user_id, and total_amount.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response with an error message if transaction creation fails,
                      or the result of handling purchased items.
        """
        transaction_data = {
            "order_id": data.get("order_id"),
            "user_id": data.get("user_id"),
            "transaction_date": datetime.now(),
            "transaction_type": "buy_now",
            "amount": data.get("total_amount"),
            "shipping_cost": 0,
            "payment_method": "credit_card",
            "payment_status": "completed",
        }
        transaction_id = TransactionMapper.create_transaction(data=transaction_data, db_session=db_session)
        if not transaction_id:
            response_data = {"error": "Error creating transaction"}
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        data.update(transaction_id=transaction_id)
        return PurchaseService.handle_items(data=data, db_session=db_session)


    @staticmethod
    def handle_items(data, db_session=None):
        """
        Handle Purchased Items

        Args:
            data (dict): Purchase data including order_id, user_id, profile, and listings.
            db_session (optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success if all items are processed,
                      or an error message if any step fails.
        """
        for listing in data.get("listings"):
            if listing.get("status") != 'active':
                response_data = {"error": "Listing is not available for purchase"}
                return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
            # TODO: sold functionality requires new data/logic of total items available for purchase
            # listing.update(status="sold")

            listing.update(purchases=(listing.get("purchases") + listing.get("quantity")))

            listing_data = {key: val for key, val in listing.items() if key != "quantity"}
            updated_rows = ListingMapper.update_listing(listing_id=listing.get("listing_id"), data=listing_data, db_session=db_session)
            if not updated_rows:
                response_data = {"error": "Error updating listing"}
                return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

            # Create order item
            order_item_data = {
                "order_id": data.get("order_id"),
                "listing_id": listing.get("listing_id"),
                "quantity": listing.get("quantity"),
                "price": listing.get("buy_now_price"),
                "total_price": listing.get("quantity") * listing.get("buy_now_price"),
            }
            order_item_id = OrderMapper.create_order_item(data=order_item_data, db_session=db_session)
            if not order_item_id:
                response_data = {"error": "Error creating order item"}
                return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

            # Create delivery for order item
            delivery_data = {
                "order_item_id": order_item_id,
                "user_id": data.get("user_id"),
                "address": data.get("profile").get("address"),
                "city": data.get("profile").get("city"),
                "state": data.get("profile").get("state"),
                "country": data.get("profile").get("country"),
                "delivery_status": "processing",
                "tracking_number": "0000000000",
                "courier": "UPS",
                "estimated_delivery_date": date.today() + timedelta(days=5),
            }
            delivery_id = DeliveryMapper.create_delivery(data=delivery_data, db_session=db_session)
            if not delivery_id:
                response_data = {"error": "Error creating delivery"}
                return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Purchase successful"}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")
