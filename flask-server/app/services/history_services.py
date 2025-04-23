from flask import jsonify, Response
from flask_login import current_user

from ..data_mappers import OrderMapper, ListingMapper, TransactionMapper, DeliveryMapper, SupportTicketMapper, ReviewMapper


class HistoryService:
    @staticmethod
    def get_user_orders(data=None, db_session=None):
        """
        Retrieve a user's order history.

        Args:
            data (dict, optional): A dictionary containing the request arguments, including user ID.
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the user's orders if found, otherwise a 404 error.
        """
        if current_user.role in ["staff", "admin"]:
            orders = OrderMapper.get_all_orders(user_id=data.get("user_id"), db_session=db_session)
        else:
            orders = OrderMapper.get_all_orders(user_id=current_user.id, db_session=db_session)

        if not orders:
            response_data = {"error": "Orders not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Orders found", "orders": orders}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def update_user_order(order_id, data, db_session=None):
        """
        Update a specific order in the user's history.

        Args:
            order_id (int): The ID of the order to update.
            data (dict): The updated data for the order.
            db_session: Optional database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        del data["created_at"]
        updated_rows = OrderMapper.update_order(order_id=order_id, data=data, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Order not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Order updated", "updated_rows": updated_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def delete_user_order(order_id, db_session=None):
        """
        Delete a specific order from the user's history.

        Args:
            order_id (int): The ID of the order to delete.
            db_session: Optional database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        deleted_rows = OrderMapper.delete_order(order_id=order_id, db_session=db_session)
        if not deleted_rows:
            response_data = {"error": "Order not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Order deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def get_user_listings(data=None, db_session=None):
        """
        Retrieve a user's listing history.

        Args:
            data (dict, optional): A dictionary containing the request arguments, including user ID.
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the user's listings if found, otherwise a 404 error.
        """
        if current_user.role not in ["staff", "admin"]:
            data.update(user_id=current_user.id)

        listings = ListingMapper.get_all_listings(args=data, db_session=db_session)

        if not listings:
            response_data = {"error": "Listings not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Listings found", "listings": listings}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def update_user_listing(listing_id, data, db_session=None):
        """
        Update a specific listing in the user's history.

        Args:
            listing_id (int): The ID of the listing to update.
            data (dict): The updated data for the listing.
            db_session: Optional database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        del data["created_at"]
        updated_rows = ListingMapper.update_listing(listing_id=listing_id, data=data, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Listing not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Listing updated", "updated_rows": updated_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def delete_user_listing(listing_id, db_session=None):
        """
        Delete a specific listing from the user's history.

        Args:
            listing_id (int): The ID of the listing to delete.
            db_session: Optional database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        deleted_rows = ListingMapper.delete_listing(listing_id=listing_id, db_session=db_session)
        if not deleted_rows:
            response_data = {"error": "Listing not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Listing deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def get_user_transactions(data=None, db_session=None):
        """
        Retrieve a user's transaction history.

        Args:
            data (dict, optional): A dictionary containing the request arguments, including user ID.
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the user's transactions if found, otherwise a 404 error.
        """
        if current_user.role in ["staff", "admin"]:
            transactions = TransactionMapper.get_all_transactions(user_id=data.get("user_id"), db_session=db_session)
        else:
            transactions = TransactionMapper.get_all_transactions(user_id=current_user.id, db_session=db_session)

        if not transactions:
            response_data = {"error": "Transactions not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Transactions found", "transactions": transactions}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def update_user_transaction(transaction_id, data, db_session=None):
        """
        Update a specific transaction in the user's history.

        Args:
            transaction_id (int): The ID of the transaction to update.
            data (dict): The updated data for the transaction.
            db_session: Optional database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        del data["created_at"]
        updated_rows = TransactionMapper.update_transaction(transaction_id=transaction_id, data=data, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Transaction not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Transaction updated", "updated_rows": updated_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def delete_user_transaction(transaction_id, db_session=None):
        """
        Delete a specific transaction from the user's history.

        Args:
            transaction_id (int): The ID of the transaction to delete.
            db_session: Optional database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        deleted_rows = TransactionMapper.delete_transaction(transaction_id=transaction_id, db_session=db_session)
        if not deleted_rows:
            response_data = {"error": "Transaction not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Transaction deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def get_user_deliveries(data=None, db_session=None):
        """
        Retrieve a user's delivery history.

        Args:
            data (dict, optional): A dictionary containing the request arguments, including user ID.
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the user's deliveries if found, otherwise a 404 error.
        """
        if current_user.role in ["staff", "admin"]:
            deliveries = DeliveryMapper.get_all_deliveries(user_id=data.get("user_id"), db_session=db_session)
        else:
            deliveries = DeliveryMapper.get_all_deliveries(user_id=current_user.id, db_session=db_session)

        if not deliveries:
            response_data = {"error": "Deliveries not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Deliveries found", "deliveries": deliveries}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def update_user_delivery(delivery_id, data, db_session=None):
        """
        Update a specific delivery in the user's history.

        Args:
            delivery_id (int): The ID of the delivery to update.
            data (dict): The updated data for the delivery.
            db_session: Optional database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        del data["created_at"]
        updated_rows = DeliveryMapper.update_delivery(delivery_id=delivery_id, data=data, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Delivery not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Delivery updated", "updated_rows": updated_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def delete_user_delivery(delivery_id, db_session=None):
        """
        Delete a specific delivery from the user's history.

        Args:
            delivery_id (int): The ID of the delivery to delete.
            db_session: Optional database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        deleted_rows = DeliveryMapper.delete_delivery(delivery_id=delivery_id, db_session=db_session)
        if not deleted_rows:
            response_data = {"error": "Delivery not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Delivery deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def get_user_support_tickets(data=None, db_session=None):
        """
        Retrieve a user's support ticket history.

        Args:
            data (dict, optional): A dictionary containing the request arguments, including user ID.
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the user's support tickets if found, otherwise a 404 error.
        """
        if current_user.role in ["staff", "admin"]:
            tickets = SupportTicketMapper.get_all_support_tickets(user_id=data.get("user_id"), db_session=db_session)
        else:
            tickets = SupportTicketMapper.get_all_support_tickets(user_id=current_user.id, db_session=db_session)

        if not tickets:
            response_data = {"error": "Support tickets not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Support tickets found", "support_tickets": tickets}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def update_user_support_ticket(ticket_id, data, db_session=None):
        """
        Update a specific support ticket in the user's history.

        Args:
            ticket_id (int): The ID of the support ticket to update.
            data (dict): The updated data for the support ticket.
            db_session: Optional database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        del data["created_at"]
        updated_rows = SupportTicketMapper.update_support_ticket(ticket_id=ticket_id, data=data, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Support ticket not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Support ticket updated", "updated_rows": updated_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def delete_user_support_ticket(ticket_id, db_session=None):
        """
        Delete a specific support ticket from the user's history.

        Args:
            ticket_id (int): The ID of the support ticket to delete.
            db_session: Optional database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        deleted_rows = SupportTicketMapper.delete_support_ticket(ticket_id=ticket_id, db_session=db_session)
        if not deleted_rows:
            response_data = {"error": "Support ticket not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Support ticket deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def get_user_reviews(data=None, db_session=None):
        """
        Retrieve a user's review history.

        Args:
            data (dict, optional): A dictionary containing the request arguments, including user ID.
            db_session (Session, optional): A database session for testing or direct queries.

        Returns:
            Response: A JSON response containing the user's reviews if found, otherwise a 404 error.
        """
        if current_user.role in ["staff", "admin"]:
            reviews = ReviewMapper.get_all_reviews(args={"user_id": data.get("user_id")}, db_session=db_session)
        else:
            reviews = ReviewMapper.get_all_reviews(args={"user_id": data.get("user_id")}, db_session=db_session)

        if not reviews:
            response_data = {"error": "Reviews not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Reviews found", "reviews": reviews}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


    @staticmethod
    def update_user_review(review_id, data, db_session=None):
        """
        Update a specific review in the user's history.

        Args:
            review_id (int): The ID of the review to update.
            data (dict): The updated data for the review.
            db_session: Optional database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        del data["created_at"]
        updated_rows = ReviewMapper.update_review(review_id=review_id, data=data, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Review not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Review updated", "updated_rows": updated_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

    @staticmethod
    def delete_user_review(review_id, db_session=None):
        """
        Delete a specific review from the user's history.

        Args:
            review_id (int): The ID of the review to delete.
            db_session: Optional database session for testing or direct queries.

        Returns:
            Response: A JSON response indicating success or failure.
        """
        deleted_rows = ReviewMapper.delete_review(review_id=review_id, db_session=db_session)
        if not deleted_rows:
            response_data = {"error": "Review not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Review deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")
