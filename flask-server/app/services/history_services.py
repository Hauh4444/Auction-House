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
    
    @staticmethod
    def get_order_by_id(order_id, db_session=None):
        """
        Retrieves an order by its ID
        """
        order = OrderMapper.get_order_by_id(order_id, db_session=db_session)
        
        if order:
            data = {"message": "Order found", "order": order}
            return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
        
        data = {"error": "Order not found"}
        return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')

    @staticmethod
    def create_order(data, db_session=None):
        """
        Creates a new order
        """
        order_id = OrderMapper.create_order(data, db_session=db_session)
        
        if order_id:
            data = {"message": "Order created successfully", "order_id": order_id}
            return Response(response=jsonify(data).get_data(), status=201, mimetype='application/json')
        
        data = {"error": "Failed to create order"}
        return Response(response=jsonify(data).get_data(), status=400, mimetype='application/json')

    @staticmethod
    def update_order(order_id, data, db_session=None):
        """
        Updates an existing order
        """
        rows_updated = OrderMapper.update_order(order_id, data, db_session=db_session)
        
        if rows_updated:
            data = {"message": "Order updated successfully"}
            return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
        
        data = {"error": "Order not found or no changes made"}
        return Response(response=jsonify(data).get_data(), status=400, mimetype='application/json')

    @staticmethod
    def delete_order(order_id, db_session=None):
        """
        Deletes an order by ID
        """
        rows_deleted = OrderMapper.delete_order(order_id, db_session=db_session)
        
        if rows_deleted:
            data = {"message": "Order deleted successfully"}
            return Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
        
        data = {"error": "Order not found"}
        return Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')
