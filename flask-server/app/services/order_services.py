from flask import jsonify, Response
import shippo
from dotenv import load_dotenv
from ..data_mappers.order_mapper import OrderMapper

# Load environment variables
load_dotenv()
shippo.api_key = os.getenv("SHIPPO_API_KEY")


class OrderService:
    @staticmethod
    def create_order(data, db_session=None):
        """
        Create a new order in Shippo and save the reference in the database.
        """
        try:
            # Create an order in Shippo
            shippo_order = shippo.Order.create(
                to_address=data["to_address"],
                from_address=data.get("from_address"),
                line_items=data.get("line_items", []),
                order_number=data["order_number"],
                order_status=data["order_status"],
                placed_at=data["placed_at"],
                total_price=data["total_price"],
                currency=data["currency"]
            )

            # Save the order details to the database
            order_data = {
                "user_id": data["user_id"],
                "order_number": data["order_number"],
                "total_price": data["total_price"],
                "order_status": data["order_status"],
                "shippo_order_id": shippo_order["object_id"]
            }
            order_id = OrderMapper.create_order(data=order_data, db_session=db_session)

            if not order_id:
                response_data = {"error": "Failed to create order"}
                return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

            response_data = {
                "message": "Order created",
                "order_id": order_id,
                "shippo_order_id": shippo_order["object_id"]
            }
            return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")

        except shippo.error.APIError as e:
            response_data = {"error": "Shippo API error", "details": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
        except Exception as e:
            response_data = {"error": "Internal server error", "details": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=500, mimetype="application/json")

    @staticmethod
    def get_order(order_id, db_session=None):
        """
        Retrieve order details from Shippo.
        """
        try:
            # Get the reference data from the database
            order_reference = OrderMapper.get_order_reference(order_id=order_id, db_session=db_session)

            if not order_reference:
                response_data = {"error": "Order not found"}
                return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

            # Use Shippo to get order details
            shippo_order = shippo.Order.retrieve(order_reference["shippo_order_id"])

            response_data = {
                "message": "Order details retrieved",
                "order": shippo_order
            }
            return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

        except shippo.error.APIError as e:
            response_data = {"error": "Shippo API error", "details": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
        except Exception as e:
            response_data = {"error": "Internal server error", "details": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=500, mimetype="application/json")

    @staticmethod
    def list_orders():
        """
        List all orders from Shippo.
        """
        try:
            orders = shippo.Order.list()
            response_data = {
                "message": "Orders retrieved",
                "orders": orders["results"]
            }
            return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

        except shippo.error.APIError as e:
            response_data = {"error": "Shippo API error", "details": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")
        except Exception as e:
            response_data = {"error": "Internal server error", "details": str(e)}
            return Response(response=jsonify(response_data).get_data(), status=500, mimetype="application/json")