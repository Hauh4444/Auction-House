from flask import Response, jsonify
from flask_login import current_user

from datetime import date, timedelta
from dotenv import load_dotenv
import stripe, os

from ..data_mappers import ProfileMapper, OrderMapper, TransactionMapper, DeliveryMapper, ListingMapper
from ..utils.logger import setup_logger

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

logger = setup_logger(name="purchase_logger", log_file="logs/purchase.log")


class PurchaseService:
    """For now, we mock most of the external data."""
    @staticmethod
    def process_payment(data: dict, db_session=None):
        """
        Process Stripe Payment

        Args:
            data (dict): Payment data including amount, currency, success_url, cancel_url, and listings.
            db_session: Optional database session to be used in tests.

        Returns:
            Response: JSON response containing either the Stripe session ID on success,
                      or an error message with the appropriate HTTP status code.
        """
        try:
            amount = int(float(data.get("amount")) * 100)
            currency, success_url, cancel_url = (data.get(k) for k in ("currency", "success_url", "cancel_url"))

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
            logger.info(msg=f"Stripe session: {session.id} created successfully")
            return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

        except stripe.error.StripeError as e:
            response_data = {"error": str(e)}
            logger.error(msg=f"Failed creating stripe session with data: {', '.join(f'{k}={v!r}' for k, v in data.items())} stripe error: {e}")
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
        except Exception as e:
            response_data = {"error": "Internal server error", "details": str(e)}
            logger.error(msg=f"Failed creating stripe session with data: {', '.join(f'{k}={v!r}' for k, v in data.items())} internal server error: {e}")
            return Response(response=jsonify(response_data).get_data(), status=500, mimetype="application/json")


    @staticmethod
    def process_purchase(data: dict, db_session=None):
        """
        Process Purchase Request

        Args:
            data (dict): Purchase data including listings and amount.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: {"status": 200} on success, or {"error": str, "status": int} on failure.
        """
        user_id, listings, amount = current_user.id, data.get("listings"), data.get("amount")

        # Retrieve the user's profile
        profile = ProfileMapper.get_profile(user_id=current_user.id, db_session=db_session)
        if not profile:
            logger.error(msg=f"Profile not found for user: {user_id}")
            return {"error": "Profile not found", "status": 404}

        logger.info(msg=f"Profile found for user: {user_id}")

        data = {"user_id": user_id, "listings": listings, "amount": amount, "profile": profile}
        return PurchaseService.create_order(data=data, db_session=db_session)


    @staticmethod
    def create_order(data: dict, db_session=None):
        """
        Create a New Order

        Args:
            data (dict): Includes user_id, listings, amount, and profile.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: {"status": 200} on success, or {"error": str, "status": int} on failure.
        """
        order_data = {"user_id": data.get("user_id"), "status": "processing"}
        order_id = OrderMapper.create_order(data=order_data, db_session=db_session)
        if not order_id:
            logger.error(msg=f"Failed creating order with data: {', '.join(f'{k}={v!r}' for k, v in order_data.items())}")
            return {"error": "Error creating order", "status": 409}

        logger.info(msg=f"Order: {order_id} created successfully with data: {', '.join(f'{k}={v!r}' for k, v in order_data.items())}")

        data.update(order_id=order_id)
        return PurchaseService.handle_items(data=data, db_session=db_session)


    @staticmethod
    def handle_items(data: dict, db_session=None):
        """
        Process Each Purchased Listing

        Args:
            data (dict): Contains user_id, profile, listings, order_id, and transaction_id.
            db_session: Optional database session to be used in tests.

        Returns:
            dict: {"status": 200} on success, or {"error": str, "status": int} on failure.
        """
        for listing in data.get("listings"):
            if listing.get("status") != "active":
                return {"error": "Listing is not available for purchase", "status": 400}
            # TODO: sold functionality requires new data/logic of total items available for purchase
            # listing.update(status="sold")

            listing.update(purchases=(listing.get("purchases") + listing.get("quantity")))

            listing_data = {key: val for key, val in listing.items() if key != "quantity" and key != "updated_at"}
            updated_rows = ListingMapper.update_listing(listing_id=listing.get("listing_id"), data=listing_data, db_session=db_session)
            if not updated_rows:
                logger.error(msg=f"Failed updating listing: {listing.get('listing_id')} with data: {', '.join(f'{k}={v!r}' for k, v in listing_data.items())}")
                return {"error": "Error updating listing", "status": 409}

            logger.info(msg=f"Listing: {listing.get('listing_id')} updated successfully with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")

            # Create order item
            order_item_data = {"order_id": data.get("order_id"), "listing_id": listing.get("listing_id"), "quantity": listing.get("quantity"),
                               "price": listing.get("buy_now_price"), "total_price": listing.get("quantity") * listing.get("buy_now_price")}
            order_item_id = OrderMapper.create_order_item(data=order_item_data, db_session=db_session)
            if not order_item_id:
                logger.error(msg=f"Failed creating order item with data: {', '.join(f'{k}={v!r}' for k, v in order_item_data.items())}")
                return {"error": "Error creating order item", "status": 409}

            logger.info(msg=f"Order item: {order_item_id} created successfully with data: {', '.join(f'{k}={v!r}' for k, v in order_item_data.items())}")

            # Create delivery for order item
            delivery_data = {"order_item_id": order_item_id, "user_id": data.get("user_id"), "address": data.get("profile").get("address"),
                             "city": data.get("profile").get("city"), "state": data.get("profile").get("state"), "country": data.get("profile").get("country"),
                             "delivery_status": "processing", "tracking_number": "0000000000", "courier": "UPS",
                             "estimated_delivery_date": date.today() + timedelta(days=5)}
            delivery_id = DeliveryMapper.create_delivery(data=delivery_data, db_session=db_session)
            if not delivery_id:
                logger.error(msg=f"Failed creating delivery with data: {', '.join(f'{k}={v!r}' for k, v in delivery_data.items())}")
                return {"error": "Error creating delivery", "status": 409}

            logger.info(msg=f"Delivery: {delivery_id} created successfully with data: {', '.join(f'{k}={v!r}' for k, v in delivery_data.items())}")

        return {"status": 200}


    @staticmethod
    def get_stripe_session_status(session_id: str, db_session=None):
        """
        Retrieve the status and details of a Stripe Checkout Session.

        Args:
            session_id (str): Stripe session ID to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            Response: JSON response with session details (e.g. customer email) and status on success,
                      or an error message with the appropriate HTTP status code on failure.
        """
        try:
            stripe_session = stripe.checkout.Session.retrieve(
                session_id,
                expand=["payment_intent"]
            )

            payment_intent = stripe_session.payment_intent
            payment_intent_id = None

            if payment_intent:
                payment_intent_id = payment_intent.get("id")

            transaction_response = PurchaseService.create_transaction(payment_intent_id=payment_intent_id, db_session=db_session)
            if not transaction_response.get("status") == 200:
                error = {"error": transaction_response.get("error")}
                status = transaction_response.get("status")
                return Response(response=jsonify(error).get_data(), status=status, mimetype="application/json")

            response_data = {
                "message": "Found stripe session",
                "customer_email": stripe_session.customer_details.email,
                "status": stripe_session.status
            }
            logger.info(msg=f"Stripe session: {session_id} found")
            return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

        except stripe.error.StripeError as e:
            response_data = {"error": str(e)}
            logger.error(msg=f"Stripe session: {session_id} error: {e}")
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
        except Exception as e:
            response_data = {"error": "Internal server error", "details": str(e)}
            logger.error(msg=f"Stripe session: {session_id} error: {e}")
            return Response(response=jsonify(response_data).get_data(), status=500, mimetype="application/json")


    @staticmethod
    def create_transaction(payment_intent_id: str, db_session=None):
        """
        Create a Transaction for the Order

        Args:
            payment_intent_id (str): Payment Intent ID.
            db_session: Database session for transactional operations.

        Returns:
            dict: {"status": 200} on success, or {"error": str, "status": int} on failure.
        """
        transaction_data = {"user_id": current_user.id, "payment_intent_id": payment_intent_id}
        transaction_id = TransactionMapper.create_transaction(data=transaction_data, db_session=db_session)
        if not transaction_id:
            logger.error(msg=f"Failed creating transaction with payment_intent_id: {payment_intent_id}")
            return {"error": "Error creating transaction", "status": 409}

        logger.info(msg=f"Transaction: {transaction_id} created successfully with payment_intent_id: {payment_intent_id}")
        return {"status": 200}


    @staticmethod
    def get_payment_method(payment_method_id: str):
        """
        Retrieve the payment method.

        Args:
            payment_method_id (str): ID of the payment method to retrieve

        Returns:
            JSON response indicating the success or failure of retrieving the payment method.
        """
        try:
            payment_method = stripe.PaymentMethod.retrieve(payment_method_id)
            response_data = {"message": "Payment method found", "payment_method": payment_method}
            logger.info(msg=f"Payment method: {payment_method_id} found")
            return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

        except stripe.error.StripeError as e:
            response_data = {"error": str(e)}
            logger.error(msg=f"Stripe error: {e}")
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
        except Exception as e:
            response_data = {"error": "Internal server error", "details": str(e)}
            logger.error(msg=f"Stripe error: {e}")
            return Response(response=jsonify(response_data).get_data(), status=500, mimetype="application/json")