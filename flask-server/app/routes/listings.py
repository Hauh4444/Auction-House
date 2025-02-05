from flask import Blueprint, request, jsonify
from ..services import ListingService

# Blueprint
listings_bp = Blueprint('listings_bp', __name__)

# GET /api/listings
@listings_bp.route('/', methods=['GET'])
def getAllListings():
    return ListingService.get_all_listings()

# GET /api/listings/{id}
@listings_bp.route('/<int:listing_id>', methods = ['GET'])
def getListing(listing_id):
    return ListingService.get_listing_by_id(listing_id)

# POST /api/listings
@listings_bp.route('/', methods=['POST'])
def createListing():
    data = request.json
    return ListingService.create_listing(data)

# PUT /api/listings/{id}
@listings_bp.route('/<int:listing_id', methods=['PUT'])
def updateListing(listing_id):
    data = request.json
    return ListingService.update_listing(listing_id, data)

# DELETE /api/listings/{id}
@listings_bp.route('/<int:listing_id>', methods=['DELETE'])
def deleteListing(listing_id):
    return ListingService.delete_listing(listing_id)