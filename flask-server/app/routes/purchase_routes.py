from flask import Blueprint, request
from flask_login import login_required

from ..services import PurchaseService

# Blueprint for purchase-related routes
bp = Blueprint("purchase_bp", __name__, url_prefix="/api/purchase")


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