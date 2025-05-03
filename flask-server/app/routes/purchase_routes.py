from flask import Blueprint, request, jsonify, Response
from flask_login import login_required, current_user

from ..services import PurchaseService
from ..utils.logger import setup_logger

# Blueprint for purchase-related routes
bp = Blueprint("purchase_bp", __name__, url_prefix="/api/purchase")

logger = setup_logger(name="purchase_logger", log_file="logs/purchase.log")


@bp.route("/", methods=["POST"])
@login_required
def process_purchase(db_session=None):
    """
    Process a purchase request.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response indicating the success or failure of the purchase.
    """
    data = request.json

    if not data.get("listings") or not data.get("amount"):
        logger.error(msg=f"Failed processing purchase with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
        return {"error": "Required data not provided", "status": 400}

    amount = int(float(data.get("amount")) * 100)
    if not amount > 0:
        response_data = {"error": "Invalid amount"}
        logger.error(msg=f"Invalid amount: {amount} for user: {current_user.id} payment")
        return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

    return PurchaseService.process_payment(data=data, db_session=db_session)


@bp.route("/status/", methods=["GET"])
@login_required
def get_stripe_session_status():
    """
    Retrieve the status of a Stripe Checkout Session.

    Returns:
        Response: JSON response containing the session status and customer email if available,
                  or an error message with the appropriate HTTP status code.
    """
    args = request.args

    if not args.get("session_id"):
        response_data = {"error": "Missing session_id parameter"}
        logger.error(msg=f"Failed retrieving stripe session with args: {', '.join(f'{k}={v!r}' for k, v in args.items())}")
        return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

    return PurchaseService.get_stripe_session_status(session_id=args.get("session_id"))