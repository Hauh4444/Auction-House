from flask import Blueprint, request, jsonify
from ..services import ListingService

# Blueprint
listings_bp = Blueprint('listings_bp', __name__)

# GET /api/listings
@listings_bp.route('/', methods=['GET'])
def getAllListings():
    listings = ListingService.get_all_listings()
    return jsonify(listings), 200

# GET /api/listings/{id}
@listings_bp.route('/<int:listing_id>', methods = ['GET'])
def getListing(listing_id):
    listing = ListingService.get_listing_by_id(listing_id)
    if listing:
        return jsonify(listing), 200
    return jsonify({"error": "Listing not found"}), 404

# POST /api/listings
@listings_bp.route('/', methods=['POST'])
def createListing():
    data = request.json
    new_listing = ListingService.create_listing(data)
    return jsonify(new_listing), 201

# PUT /api/listings/{id}
@listings_bp.route('/<int:listing_id', methods=['PUT'])
def updateListing(listing_id):
    data = request.json
    updated_listing = ListingService.update_listing(listing_id, data)
    if updated_listing:
        return jsonify(updated_listing), 200
    return jsonify({"error": "Listing not found or update failed"}), 404

# DELETE /api/listings/{id}
@listings_bp.route('/<int:listing_id>', methods=['DELETE'])
def deleteListing(listing_id):
    success = ListingService.delete_listing(listing_id)
    if success:
        return jsonify({"message": "Listing deleted"}), 200
    return jsonify({"error": "Listing not found"}), 404