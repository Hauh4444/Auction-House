import requests
import os
from flask import Blueprint, request
from flask_login import login_required
from ..services import ListingService

# Blueprint for listing-related routes
bp = Blueprint("listings_bp", __name__, url_prefix="/api/listings")

# PostHog API configuration
POSTHOG_API_KEY = os.getenv("POST_HOG_API_KEY")
POSTHOG_API_URL = "https://app.posthog.com/capture/"

def capture_posthog_event(event_name, properties, distinct_id):
    """
    Helper function to send events to PostHog.
    """
    payload = {
        "api_key": POSTHOG_API_KEY,
        "event": event_name,
        "properties": properties,
        "distinct_id": distinct_id,
    }
    response = requests.post(POSTHOG_API_URL, json=payload)
    return response

# GET /api/listings/
@bp.route("/", methods=["GET"])
def get_all_listings(db_session=None):
    """
    Retrieve all listings with optional filters.
    """
    args = request.args
    listings = ListingService.get_all_listings(args=args, db_session=db_session)
    
    # Track this event in PostHog
    posthog_properties = {
        "filter_args": str(args),
    }
    capture_posthog_event("view_listings", posthog_properties, distinct_id="anonymous")
    
    return listings


# GET /api/listings/{id}/
@bp.route("/<int:listing_id>/", methods=["GET"])
def get_listing(listing_id, db_session=None):
    """
    Retrieve a single listing by its ID.
    """
    listing = ListingService.get_listing_by_id(listing_id=listing_id, db_session=db_session)
    
    # Track this event in PostHog
    posthog_properties = {
        "listing_id": listing_id,
        "listing_name": listing.get("name", "Unknown"),
    }
    capture_posthog_event("view_listing", posthog_properties, distinct_id="anonymous")
    
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
    
    # Track this event in PostHog
    posthog_properties = {
        "listing_id": new_listing.id,
        "listing_name": new_listing.name,
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
    
    # Track this event in PostHog
    posthog_properties = {
        "listing_id": listing_id,
        "listing_name": updated_listing.name,
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
    
    # Track this event in PostHog
    posthog_properties = {
        "listing_id": listing_id,
        "user_id": current_user.id,
    }
    capture_posthog_event("delete_listing", posthog_properties, distinct_id=current_user.id)
    
    return deleted_listing
