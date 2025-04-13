from flask import Blueprint, request, jsonify
from flask_login import login_required
import stripe

from ..services import PurchaseService

bp = Blueprint("purchase_bp", __name__, url_prefix="/api/purchase")


@bp.route('/', methods=['POST'])
@login_required
def purchase(db_session=None):
    """
    Process a purchase request.

    Args:
        db_session (optional): A database session for testing or direct queries.

    Returns:
        JSON response indicating the success or failure of the purchase.
    """
    data = request.json
    return PurchaseService.process_purchase(data=data, db_session=db_session)


@bp.route('/create-stripe-session', methods=['POST'])
@login_required
def create_stripe_session():
    data = request.json
    return PurchaseService.process_payment(data)


@bp.route('/stripe-session-status', methods=['POST'])
@login_required
def stripe_session_status():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({"error": "Missing session_id parameter"}), 400
    
    try:
        session = stripe.checkout.Session.retrieve(session_id)

        return jsonify({
            "status": session.status,
            "customer_email": session.customer_details.email if session.customer_details else None
        })
    except stripe.error.StripeError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500