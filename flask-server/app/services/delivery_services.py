from flask import jsonify, Response
from ..data_mappers.delivery_mapper import DeliveryMapper


class DeliveryService:
    @staticmethod
    def get_user_deliveries(data=None, db_session=None):
        """
        Retrieve a user's delivery history.
        """
        deliveries = DeliveryMapper.get_all_deliveries(user_id=data.get("user_id"), db_session=db_session)

        if not deliveries:
            response_data = {"error": "Deliveries not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Deliveries found", "deliveries": deliveries}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

    @staticmethod
    def get_delivery_by_id(delivery_id, db_session=None):
        """
        Retrieve a specific delivery by its ID.
        """
        delivery = DeliveryMapper.get_delivery_by_id(delivery_id=delivery_id, db_session=db_session)

        if not delivery:
            response_data = {"error": "Delivery not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Delivery found", "delivery": delivery}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

    @staticmethod
    def create_delivery(data, db_session=None):
        """
        Create a new delivery record.
        """
        delivery_id = DeliveryMapper.create_delivery(data=data, db_session=db_session)

        if not delivery_id:
            response_data = {"error": "Failed to create delivery"}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        response_data = {"message": "Delivery created", "delivery_id": delivery_id}
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")

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
    def track_delivery(tracking_code):
        """
        Track a delivery using AfterShip.
        """
        tracker = DeliveryMapper.track_delivery(tracking_code=tracking_code)

        if not tracker:
            response_data = {"error": "Tracking information not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Tracking details retrieved", "tracker": tracker}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")