from flask import Blueprint, request
from flask_login import login_required

from ..services import ListingService

# Blueprint for listing-related routes
bp = Blueprint("listings_bp", __name__, url_prefix="/api/listings")


# GET /api/listings
@bp.route("/", methods=["GET"])
def get_all_listings(db_session=None):
    """
    Retrieve all listings with optional filters.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing a list of all listings.
    """
    args = request.args
    return ListingService.get_all_listings(args=args, db_session=db_session)


# GET /api/listings/{id}
@bp.route("/<int:listing_id>", methods=["GET"])
def get_listing(listing_id, db_session=None):
    """
    Retrieve a single listing by its ID.

    Args:
        listing_id (int): The ID of the listing to retrieve.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing listing details.
    """
    return ListingService.get_listing_by_id(listing_id=listing_id, db_session=db_session)


# POST /api/listings
@bp.route("/", methods=["POST"])
@login_required
def create_listing(db_session=None):
    """Create a new listing.

    Args:
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload with listing details.

    Returns:
        JSON response containing the created listing.
    """
    data = request.json
    return ListingService.create_listing(data=data, db_session=db_session)


# PUT /api/listings/{id}
@bp.route("/<int:listing_id>", methods=["PUT"])
@login_required
def update_listing(listing_id, db_session=None):
    """Update an existing listing by its ID.

    Args:
        listing_id (int): The ID of the listing to update.
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload with updated listing details.

    Returns:
        JSON response containing the updated listing.
    """
    data = request.json
    return ListingService.update_listing(listing_id=listing_id, data=data, db_session=db_session)


# DELETE /api/listings/{id}
@bp.route("/<int:listing_id>", methods=["DELETE"])
@login_required
def deleteListing(listing_id, db_session=None):
    """Delete a listing by its ID.

    Args:
        listing_id (int): The ID of the listing to delete.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response indicating the deletion status.
    """
    return ListingService.delete_listing(listing_id=listing_id, db_session=db_session)
