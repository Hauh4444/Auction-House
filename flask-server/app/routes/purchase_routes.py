from flask import Blueprint, request, jsonify
from app.services.purchase_services import PurchaseService

purchase_bp = Blueprint('purchase', __name__)

@purchase_bp.route('/purchase', methods=['POST'])
def purchase():
    data = request.get_json()
    listing_id = data.get('listing_id')
    user_id = data.get('user_id')
    if not listing_id or not user_id:
        return jsonify({"error": "Listing ID and User ID are required"}), 400
    return PurchaseService.process_purchase(listing_id, user_id)