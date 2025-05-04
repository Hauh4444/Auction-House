from flask import Blueprint, request
from flask_login import login_required
from ..services.purchase_services import PurchaseService

bp = Blueprint("purchase", __name__, url_prefix="/api/purchase")


@bp.route('/', methods=['POST'])
@login_required
def process_purchase(db_session=None):
    """
    Process a purchase request.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response indicating the success or failure of the purchase.
    """
    data = request.json
    return PurchaseService.process_payment(data=data, db_session=db_session)


@bp.route('/status/', methods=['GET'])
@login_required
def get_stripe_session_status():
    args = request.args
    return PurchaseService.get_stripe_session_status(args=args)


@bp.route("/order/<int:order_id>", methods=["GET"])
@login_required
def get_order(order_id):
    return PurchaseService.get_order(order_id=order_id)

@bp.route("/transaction/<int:transaction_id>", methods=["GET"])
@login_required
def get_transaction(transaction_id):
    return PurchaseService.get_transaction(transaction_id=transaction_id)

@bp.route("/order-item/<int:order_item_id>", methods=["GET"])
@login_required
def get_order_item(order_item_id):
    return PurchaseService.get_order_item(order_item_id=order_item_id)

@bp.route("/delivery/<int:delivery_id>", methods=["GET"])
@login_required
def get_delivery(delivery_id):
    return PurchaseService.get_delivery(delivery_id=delivery_id)
