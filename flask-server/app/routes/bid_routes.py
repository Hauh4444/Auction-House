from flask import Blueprint, request, jsonify, Response

from ..services import BidService
from ..utils.logger import setup_logger

# Blueprint for bid-related routes
bp = Blueprint('bid_routes', __name__, url_prefix='/api/bids')

logger = setup_logger(name="bid_logger", log_file="logs/bid.log")


@bp.route('/', methods=['GET'])
def get_all_bids(db_session=None):
    """
    Get all bids.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response with a list of all bids.
    """
    return BidService.get_all_bids(db_session=db_session)


@bp.route('/<int:bid_id>', methods=['GET'])
def get_bid_by_id(bid_id, db_session=None):
    """
    Get bid by its id.

    Args:
        bid_id (int): The ID of the bid to retrieve.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response with the bid details if found, or a 404 error if not found.
    """
    return BidService.get_bid_by_id(bid_id=bid_id, db_session=db_session)


@bp.route('/', methods=['POST'])
def create_bid(db_session=None):
    """
    Create a new bid.

    Args:
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload containing bid data (e.g., item_id, new_bid, etc.).

    Returns:
        JSON response with status of the bid posting operation.
    """
    data = request.json

    if not data.get("user") or not data.get("amount"):
        response_data = {"error": "User and amount are required"}
        logger.error(msg=f"Failed creating bid with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
        return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

    return BidService.create_bid(data=data, db_session=db_session)