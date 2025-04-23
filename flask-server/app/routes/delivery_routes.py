from flask import Blueprint, request
from flask_login import login_required
from ..services.delivery_services import DeliveryService

bp = Blueprint("deliveries", __name__, url_prefix="/api/deliveries")


@bp.route("/", methods=["GET"])
@login_required
def get_user_deliveries():
    """
    Retrieve a user's delivery history.
    """
    data = request.args.to_dict()
    return DeliveryService.get_user_deliveries(data=data)


@bp.route("/<int:delivery_id>", methods=["GET"])
@login_required
def get_delivery_by_id(delivery_id):
    """
    Retrieve a specific delivery by its ID.
    """
    return DeliveryService.get_delivery_by_id(delivery_id=delivery_id)


@bp.route("/", methods=["POST"])
@login_required
def create_delivery():
    """
    Create a new delivery.
    """
    data = request.json
    return DeliveryService.create_delivery(data=data)


@bp.route("/track/<string:tracking_code>", methods=["GET"])
@login_required
def track_delivery(tracking_code):
    """
    Track a delivery by its tracking code.
    """
    return DeliveryService.track_delivery(tracking_code=tracking_code)


@bp.route("/<int:delivery_id>", methods=["PUT"])
@login_required
def update_user_delivery(delivery_id):
    """
    Update a specific delivery in the user's history.
    """
    data = request.json
    return DeliveryService.update_user_delivery(delivery_id=delivery_id, data=data)


@bp.route("/<int:delivery_id>", methods=["DELETE"])
@login_required
def delete_user_delivery(delivery_id):
    """
    Delete a specific delivery from the user's history.
    """
    return DeliveryService.delete_user_delivery(delivery_id=delivery_id)