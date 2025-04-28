from flask import Blueprint, request
from flask_login import login_required
import posthog

from ..services import ListingService

# Blueprint for listing-related routes
bp = Blueprint("listings_bp", __name__, url_prefix="/api/listings")

# Initialize PostHog
posthog.api_key = "your_posthog_api_key"  # Replace with your PostHog API key


# Utility function to capture PostHog event
def capture_posthog_event(event_name, properties, distinct_id):
    posthog.capture(
        distinct_id=distinct_id,
        event=event_name,
        properties=properties
    )


# GET /api/listings/
@bp.route("/", methods=["GET"])
def get_all_listings(db_session=None):
    """
    Retrieve all listings with optional filters.
    """
    args = request.args
    listings = ListingService.get_all_listings(args=args, db_session=db_session)

    # Track views for all products in the listings
    for listing in listings:
        posthog_properties = {
            "listing_id": listing["id"],
            "listing_name": listing["name"],
            "listing_category": listing["category"],
            "listing_price": listing["price"],
            "listing_status": listing["status"],  # Auction status
        }
        capture_posthog_event("view_listing", posthog_properties, distinct_id="anonymous")  # Or current_user.id if authenticated

    return listings


# GET /api/listings/{id}/
@bp.route("/<int:listing_id>/", methods=["GET"])
def get_listing(listing_id, db_session=None):
    """
    Retrieve a single listing by its ID.
    """
    # Retrieve the product details
    listing = ListingService.get_listing_by_id(listing_id=listing_id, db_session=db_session)

    # Log the product view event to PostHog
    posthog_properties = {
        "listing_id": listing.id,
        "listing_name": listing.name,
        "listing_category": listing.category,
        "listing_price": listing.price,
        "listing_status": listing.status,  # Auction status
        "views": listing.views,
    }
    capture_posthog_event("view_listing", posthog_properties, distinct_id="anonymous")  # Or current_user.id if authenticated

    # Increment the view count for the listing in the database
    listing.views += 1
    db_session.commit()

    return listing


# POST /api/listings/
@bp.route("/", methods=["POST"])
@login_required
def create_listing(db_session=None):
    """
    Create a new listing.
    """
    data = request.json
    new_listing = ListingService.create_listing(data=data, db_session=db_session)

    # Log product creation event to PostHog
    posthog_properties = {
        "listing_id": new_listing.id,
        "listing_name": new_listing.name,
        "listing_category": new_listing.category,
        "listing_price": new_listing.price,
        "listing_status": new_listing.status,
        "user_id": current_user.id,
    }
    capture_posthog_event("create_listing", posthog_properties, distinct_id=current_user.id)

    return new_listing


# PUT /api/listings/{id}/
@bp.route("/<int:listing_id>/", methods=["PUT"])
@login_required
def update_listing(listing_id, db_session=None):
    """
    Update an existing listing by its ID.
    """
    data = request.json
    updated_listing = ListingService.update_listing(listing_id=listing_id, data=data, db_session=db_session)

    # Log product update event to PostHog
    posthog_properties = {
        "listing_id": listing_id,
        "listing_name": updated_listing.name,
        "listing_category": updated_listing.category,
        "listing_price": updated_listing.price,
        "listing_status": updated_listing.status,
        "user_id": current_user.id,
    }
    capture_posthog_event("update_listing", posthog_properties, distinct_id=current_user.id)

    return updated_listing


# DELETE /api/listings/{id}/
@bp.route("/<int:listing_id>/", methods=["DELETE"])
@login_required
def delete_listing(listing_id, db_session=None):
    """
    Delete a listing by its ID.
    """
    deleted_listing = ListingService.delete_listing(listing_id=listing_id, db_session=db_session)

    # Log product deletion event to PostHog
    posthog_properties = {
        "listing_id": listing_id,
        "listing_name": deleted_listing.name,
        "listing_category": deleted_listing.category,
        "listing_price": deleted_listing.price,
        "listing_status": deleted_listing.status,
        "user_id": current_user.id,
    }
    capture_posthog_event("delete_listing", posthog_properties, distinct_id=current_user.id)

    return deleted_listing
