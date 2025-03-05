from flask import jsonify, Response
from ..data_mappers import OrderMapper


class HistoryService:
    # TODO: Services that align with each route
    #       Each service will call the appropriate, already created data mappers
    #       DO NOT CREATE NEW DATA MAPPERS FOR THESE SERVICES USE EXISTING ONES


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
            response = Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
            return response

        data = {"error": "Orders not found"}
        response = Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')
        return response
