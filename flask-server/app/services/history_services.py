from flask import jsonify, Response, session

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
        if session.get("role") in ["staff", "admin"]:
            orders = OrderMapper.get_all_orders(user_id=data.get("user_id"), db_session=db_session)
        else:
            orders = OrderMapper.get_all_orders(user_id=session.get("user_id"), db_session=db_session)

        if not orders:
            response_data = {"error": "Orders not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Orders found", "orders": orders}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


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
        if session.get("role") in ["staff", "admin"]:
            listings = ListingMapper.get_all_user_listings(user_id=data.get("user_id"), db_session=db_session)
        else:
            listings = ListingMapper.get_all_user_listings(user_id=session.get("user_id"), db_session=db_session)

        if not listings:
            response_data = {"error": "Listings not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Listings found", "listings": listings}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


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
        if session.get("role") in ["staff", "admin"]:
            transactions = TransactionMapper.get_all_transactions(user_id=data.get("user_id"), db_session=db_session)
        else:
            transactions = TransactionMapper.get_all_transactions(user_id=session.get("user_id"), db_session=db_session)

        if not transactions:
            response_data = {"error": "Transactions not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Transactions found", "transactions": transactions}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


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
        if session.get("role") in ["staff", "admin"]:
            deliveries = DeliveryMapper.get_all_deliveries(user_id=data.get("user_id"), db_session=db_session)
        else:
            deliveries = DeliveryMapper.get_all_deliveries(user_id=session.get("user_id"), db_session=db_session)

        if not deliveries:
            response_data = {"error": "Deliveries not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Deliveries found", "deliveries": deliveries}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


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
        if session.get("role") in ["staff", "admin"]:
            tickets = SupportTicketMapper.get_all_support_tickets(user_id=data.get("user_id"), db_session=db_session)
        else:
            tickets = SupportTicketMapper.get_all_support_tickets(user_id=session.get("user_id"), db_session=db_session)

        if not tickets:
            response_data = {"error": "Support tickets not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Support tickets found", "support_tickets": tickets}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')


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
        if session.get("role") in ["staff", "admin"]:
            reviews = ReviewMapper.get_all_reviews(args={"user_id": data.get("user_id")}, db_session=db_session)
        else:
            reviews = ReviewMapper.get_all_reviews(args={"user_id": data.get("user_id")}, db_session=db_session)

        if not reviews:
            response_data = {"error": "Reviews not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype='application/json')

        response_data = {"message": "Reviews found", "reviews": reviews}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype='application/json')
