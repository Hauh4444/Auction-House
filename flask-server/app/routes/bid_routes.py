from flask import Blueprint, request, jsonify
import socketio
from ..services import BidService  # Import the BidService class for business logic

# Define the Blueprint with the URL prefix '/api/bids'
bp = Blueprint('bid_routes', __name__, url_prefix='/api/bids')


@bp.route('/post_bid', methods=['POST'])
def post_bid():
    """
    Endpoint for posting a new bid. This triggers both saving the bid and broadcasting it in real-time.

    Expects:
        JSON payload containing bid data (e.g., item_id, new_bid, etc.).

    Returns:
        JSON response with status of the bid posting operation.
    """
    data = request.get_json()  # Get bid data from the request body

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Use BidService to handle business logic (e.g., save the bid)
    result = BidService.post_bid(data)

    if result['status'] == 'success':
        socket = socketio.AsyncServer()

        # Emit a 'new_bid' event via SocketIO to notify all connected clients
        socket.emit('new_bid', {
            'item_id': result['item_id'],
            'new_bid': result['new_bid']
        })
        return jsonify(result), 200
    else:
        return jsonify(result), 400


@bp.route('/get_bid/<int:bid_id>', methods=['GET'])
def get_bid(bid_id):
    """
    Endpoint to retrieve a specific bid by its ID.

    Args:
        bid_id (int): The ID of the bid to retrieve.

    Returns:
        JSON response with the bid details if found, or a 404 error if not found.
    """
    bid = BidService.get_bid_by_id(bid_id)
    if bid:
        return jsonify(bid), 200
    else:
        return jsonify({"error": "Bid not found"}), 404


@bp.route('/get_all_bids', methods=['GET'])
def get_all_bids():
    """
    Endpoint to retrieve all bids.

    Returns:
        JSON response with a list of all bids.
    """
    bids = BidService.get_all_bids()
    return jsonify(bids), 200
