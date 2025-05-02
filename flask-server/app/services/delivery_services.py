from flask import jsonify, Response
import shippo
from dotenv import load_dotenv
from ..data_mappers.delivery_mapper import DeliveryMapper

# Load environment variables
load_dotenv()
shippo.api_key = os.getenv("SHIPPO_API_KEY")


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
        Create a new delivery record in the database and generate a shipment using Shippo.
        """
        try:
            # Create a shipment using Shippo
            shipment = shippo.Shipment.create(
                address_from=data["from_address"],
                address_to=data["to_address"],
                parcels=[data["parcel"]],
                asynchronous=False
            )

            # Extract tracking details
            tracking_number = shipment["tracking"]["tracking_number"]
            courier = shipment["tracking"]["carrier"]
            tracking_url_provider = shipment["tracking"]["tracking_url"]

            # Save the delivery details to the database
            delivery_data = {
                "user_id": data["user_id"],
                "tracking_number": tracking_number,
                "courier": courier,
                "tracking_url_provider": tracking_url_provider
            }
            delivery_id = DeliveryMapper.create_delivery(data=delivery_data, db_session=db_session)

            if not delivery_id:
                response_data = {"error": "Failed to create delivery"}
                return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

            response_data = {
                "message": "Delivery created",
                "delivery_id": delivery_id,
                "tracking_number": tracking_number,
                "courier": courier,
                "tracking_url_provider": tracking_url_provider
            }
            return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")

        except shippo.error.APIError as e:
            response_data = {"error": "Shippo API error", "details": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
        except Exception as e:
            response_data = {"error": "Internal server error", "details": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=500, mimetype="application/json")

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

    @staticmethod
    def get_delivery(delivery_id, db_session=None):
        """
        Retrieve delivery tracking details using Shippo.
        """
        try:
            # Get the reference data from the database
            delivery_reference = DeliveryMapper.get_delivery_reference(delivery_id=delivery_id, db_session=db_session)

            if not delivery_reference:
                response_data = {"error": "Delivery not found"}
                return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

            # Use Shippo to get tracking details
            tracking_number = delivery_reference["tracking_number"]
            courier = delivery_reference["courier"]
            tracking_status = shippo.Track.get(carrier=courier, tracking_number=tracking_number)

            response_data = {
                "message": "Tracking details retrieved",
                "tracking_status": tracking_status
            }
            return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

        except shippo.error.APIError as e:
            response_data = {"error": "Shippo API error", "details": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
        except Exception as e:
            response_data = {"error": "Internal server error", "details": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=500, mimetype="application/json")