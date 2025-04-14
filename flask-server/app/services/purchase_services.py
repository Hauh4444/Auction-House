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
    """For now, we mock most of the external data."""
    @staticmethod
    def process_payment(data, db_session=None):
        """
        Process Stripe Payment

        Args:
            data (dict): Payment data including amount, currency, success_url, cancel_url, and listings.
            db_session (optional): Database session for transactional operations.

        Returns:
            Response: JSON response containing either the Stripe session ID on success,
                      or an error message with the appropriate HTTP status code.
        """
        try:
            amount = int(float(data.get("amount")) * 100)
            currency, success_url, cancel_url = (data.get(k) for k in ("currency", "success_url", "cancel_url"))

            if not amount > 0:
                response_data = {"error": "Invalid amount"}
                return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

            session = stripe.checkout.Session.create(
                payment_method_types = ["card"],
                line_items = [{
                    "price_data": {
                        "currency": currency,
                        "product_data": {"name": "Purchase from Marketplace"},
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }],
                mode = "payment",
                success_url = success_url,
                cancel_url = cancel_url,
            )

            data = {"listings": data.get("listings"), "amount": data.get("amount")}
            response_data = PurchaseService.process_purchase(data=data, db_session=db_session)
            if not response_data.get("status") == 200:
                error = {"error": response_data.get("error")}
                status = response_data.get("status")
                return Response(response=jsonify(error).get_data(), status=status, mimetype="application/json")

            response_data = {"message": "Stripe session created", "id": session.id}
            return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

        except stripe.error.StripeError as e:
            response_data = {"error": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
        except Exception as e:
            response_data = {"error": "Internal server error", "details": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=500, mimetype="application/json")


    @staticmethod
    def process_purchase(data, db_session=None):
        """
        Process Purchase Request

        Args:
            data (dict): Purchase data including listings and amount.
            db_session (optional): Database session for transactional operations.

        Returns:
            dict: {"status": 200} on success, or {"error": str, "status": int} on failure.
        """
        user_id, listings, amount = current_user.id, data.get('listings'), data.get("amount")
        if not listings or not amount:
            return {"error": "Required data not provided", "status": 400},

        # Retrieve the user's profile
        profile = ProfileService.get_profile(db_session=db_session).json.get("profile")
        if not profile:
            return {"error": "Profile not found", "status": 404}

        data = {"user_id": user_id, "listings": listings, "amount": amount, "profile": profile}
        return PurchaseService.create_order(data=data, db_session=db_session)


    @staticmethod
    def create_order(data, db_session=None):
        """
        Create a New Order

        Args:
            data (dict): Includes user_id, listings, amount, and profile.
            db_session (optional): Database session for transactional operations.

        Returns:
            dict: {"status": 200} on success, or {"error": str, "status": int} on failure.
        """
        order_data = {"user_id": data.get("user_id"), "order_date": datetime.now(), "status": "processing"}
        order_id = OrderMapper.create_order(data=order_data, db_session=db_session)
        if not order_id:
            return {"error": "Error creating order", "status": 409}

        data.update(order_id=order_id)
        return PurchaseService.create_transaction(data=data, db_session=db_session)


    @staticmethod
    def create_transaction(data, db_session=None):
        """
        Create a Transaction for the Order

        Args:
            data (dict): Includes order_id, user_id, amount, and related data.
            db_session (optional): Database session for transactional operations.

        Returns:
            dict: {"status": 200} on success, or {"error": str, "status": int} on failure.
        """
        transaction_data = {"order_id": data.get("order_id"), "user_id": data.get("user_id"), "transaction_date": datetime.now(), "transaction_type": "buy_now",
                            "amount": data.get("amount"), "shipping_cost": 0, "payment_method": "credit_card", "payment_status": "completed"}
        transaction_id = TransactionMapper.create_transaction(data=transaction_data, db_session=db_session)
        if not transaction_id:
            return {"error": "Error creating transaction", "status": 409}

        data.update(transaction_id=transaction_id)
        return PurchaseService.handle_items(data=data, db_session=db_session)


    @staticmethod
    def handle_items(data, db_session=None):
        """
        Process Each Purchased Listing

        Args:
            data (dict): Contains user_id, profile, listings, order_id, and transaction_id.
            db_session (optional): Database session for transactional operations.

        Returns:
            dict: {"status": 200} on success, or {"error": str, "status": int} on failure.
        """
        for listing in data.get("listings"):
            if listing.get("status") != 'active':
                return {"error": "Listing is not available for purchase", "status": 400}
            # TODO: sold functionality requires new data/logic of total items available for purchase
            # listing.update(status="sold")

            listing.update(purchases=(listing.get("purchases") + listing.get("quantity")))

            listing_data = {key: val for key, val in listing.items() if key != "quantity"}
            updated_rows = ListingMapper.update_listing(listing_id=listing.get("listing_id"), data=listing_data, db_session=db_session)
            if not updated_rows:
                return {"error": "Error updating listing", "status": 409}

            # Create order item
            order_item_data = {"order_id": data.get("order_id"), "listing_id": listing.get("listing_id"), "quantity": listing.get("quantity"),
                               "price": listing.get("buy_now_price"), "total_price": listing.get("quantity") * listing.get("buy_now_price")}
            order_item_id = OrderMapper.create_order_item(data=order_item_data, db_session=db_session)
            if not order_item_id:
                return {"error": "Error creating order item", "status": 409}

            # Create delivery for order item
            delivery_data = {"order_item_id": order_item_id, "user_id": data.get("user_id"), "address": data.get("profile").get("address"),
                             "city": data.get("profile").get("city"), "state": data.get("profile").get("state"), "country": data.get("profile").get("country"),
                             "delivery_status": "processing", "tracking_number": "0000000000", "courier": "UPS",
                             "estimated_delivery_date": date.today() + timedelta(days=5)}
            delivery_id = DeliveryMapper.create_delivery(data=delivery_data, db_session=db_session)
            if not delivery_id:
                return {"error": "Error creating delivery", "status": 409}

        return {"status": 200}


    @staticmethod
    def get_stripe_session_status(args):
        session_id = args.get('session_id')
        if not session_id:
            response_data = {"error": "Missing session_id parameter"}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        try:
            stripe_session = stripe.checkout.Session.retrieve(session_id)

            response_data = {"message": "Found stripe session", "customer_email": stripe_session.customer_details.email if stripe_session.customer_details else None}
            return Response(response=jsonify(response_data).get_data(), status=stripe_session.status, mimetype="application/json")

        except stripe.error.StripeError as e:
            response_data = {"error": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
        except Exception as e:
            response_data = {"error": "Internal server error", "details": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=500, mimetype="application/json")