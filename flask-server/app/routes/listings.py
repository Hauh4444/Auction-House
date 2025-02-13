from flask import Blueprint, request
from ..services import ListingService

# Blueprint for listing-related routes
listings_bp = Blueprint('listings_bp', __name__)


# GET /api/listings
@listings_bp.route('/', methods=['GET'])
def getAllListings():
    """Retrieve all listings with optional filters.

    Returns:
        JSON response containing a list of all listings.
    """
    return ListingService.get_all_listings(request)


# GET /api/listings/{id}
@listings_bp.route('/<int:listing_id>', methods=['GET'])
def getListing(listing_id):
    """Retrieve a single listing by its ID.

    Args:
        listing_id (int): The ID of the listing to retrieve.

    Returns:
        JSON response containing listing details.
    """
    return ListingService.get_listing_by_id(listing_id)


# POST /api/listings
@listings_bp.route('/', methods=['POST'])
def createListing():
    """Create a new listing.

    Expects:
        JSON payload with listing details.

    Returns:
        JSON response containing the created listing.
    """
    data = request.json
    return ListingService.create_listing(data)


# PUT /api/listings/{id}
@listings_bp.route('/<int:listing_id>', methods=['PUT'])
def updateListing(listing_id):
    """Update an existing listing by its ID.

    Args:
        listing_id (int): The ID of the listing to update.

    Expects:
        JSON payload with updated listing details.

    Returns:
        JSON response containing the updated listing.
    """
    data = request.json
    return ListingService.update_listing(listing_id, data)


# DELETE /api/listings/{id}
@listings_bp.route('/<int:listing_id>', methods=['DELETE'])
def deleteListing(listing_id):
    """Delete a listing by its ID.

    Args:
        listing_id (int): The ID of the listing to delete.

    Returns:
        JSON response indicating the deletion status.
    """
    return ListingService.delete_listing(listing_id)
