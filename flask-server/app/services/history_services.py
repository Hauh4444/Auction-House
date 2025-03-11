from flask import jsonify, Response

from ..data_mappers import OrderMapper, ListingMapper, TransactionMapper, DeliveryMapper, SupportTicketMapper, ReviewMapper


class HistoryService:
    @staticmethod
    def get_user_orders(user_id, db_session=None):
        """
        Retrieves a user's orders

        Args:
            user_id (int): The ID of the user to retrieve history of.
            db_session: Optional database session to be used in tests.

        Returns:
            A response object with the orders data if found, otherwise a 404 error with a message.
        """
        orders = OrderMapper.get_all_orders(user_id=user_id, db_session=db_session)

        if orders:
            data = {"message": "Orders found", "orders": orders}
            return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')

        data = {"error": "Orders not found"}
        return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')


    @staticmethod
    def get_user_listings(user_id, db_session=None):
        """
        Retrieves a user's listings
        """
        listings = ListingMapper.get_all_listings(user_id=user_id, db_session=db_session)

        if listings:
            data = {"message": "Listings found", "listings": listings}
            return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')

        data = {"error": "Listings not found"}
        return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')


    @staticmethod
    def get_user_transactions(user_id, db_session=None):
        """
        Retrieves a user's transactions
        """
        transactions = TransactionMapper.get_all_transactions(buyer_id=user_id, db_session=db_session)

        if transactions:
            data = {"message": "Transactions found", "transactions": transactions}
            return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')

        data = {"error": "Transactions not found"}
        return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')


    @staticmethod
    def get_user_deliveries(user_id, db_session=None):
        """
        Retrieves a user's deliveries
        """
        deliveries = DeliveryMapper.get_all_deliveries(user_id=user_id, db_session=db_session)

        if deliveries:
            data = {"message": "Deliveries found", "deliveries": deliveries}
            return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')

        data = {"error": "Deliveries not found"}
        return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')


    @staticmethod
    def get_user_support_tickets(user_id, db_session=None):
        """
        Retrieves a user's support tickets
        """
        tickets = SupportTicketMapper.get_all_support_tickets(user_id=user_id, db_session=db_session)

        if tickets:
            data = {"message": "Support tickets found", "support_tickets": tickets}
            return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')

        data = {"error": "Support tickets not found"}
        return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')


    @staticmethod
    def get_user_reviews(user_id, db_session=None):
        """
        Retrieves a user's reviews
        """
        args = {"user_id": user_id}
        reviews = ReviewMapper.get_all_reviews(args=args, db_session=db_session)

        if reviews:
            data = {"message": "Reviews found", "reviews": reviews}
            return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')

        data = {"error": "Reviews not found"}
        return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')