from flask import Blueprint, request, jsonify
from bid_services import BidService

bid_routes = Blueprint('bid_routes', __name__)

@bid_routes.route('/post_bid', methods=['POST'])
def post_bid():
    """
    Endpoint for posting a new bid. Will trigger both saving the bid and broadcasting it in real-time.
    """
    data = request.get_json()  # Get bid data from the request body

    if not data:
        return jsonify({"error": "No data provided"}), 400

    return BidService.post_bid(data)

@bid_routes.route('/get_bid/<int:bid_id>', methods=['GET'])
def get_bid(bid_id):
    """
    Endpoint to retrieve a specific bid by its ID.
    """
    return BidService.get_bid_by_id(bid_id)

@bid_routes.route('/get_all_bids', methods=['GET'])
def get_all_bids():
    """
    Endpoint to retrieve all bids.
    """
    return BidService.get_all_bids()
