from flask import jsonify, Response
from flask_login import current_user

from ..data_mappers import ListingMapper
from ..utils.logger import setup_logger
from ..utils.auction_tasks import end_auction_task

logger = setup_logger(name="listing_logger", log_file="logs/listing.log")


class ListingService:
    @staticmethod
    def get_all_listings(args: dict, db_session=None):
        """
        Retrieves a list of all listings, with optional filtering and sorting based on query parameters.

        Args:
            args (dict): Dictionary of query parameters.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object containing the list of listings with a 200 status code.
        """
        listings = ListingMapper.get_all_listings(args=args, db_session=db_session)
        if not listings:
            response_data = {"error": "No listings found"}
            logger.error(msg=f"No listings found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Listings found", "listings": listings}
        logger.info(msg=f"Listings found: {[listing.get('listing_id') for listing in listings]}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")
        

    @staticmethod
    def get_listing_by_id(listing_id: int, db_session=None):
        """
        Retrieves a specific listing by its ID.

        Args:
            listing_id: The ID of the listing to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the listing data if found, otherwise a 404 error with a message.
        """
        listing = ListingMapper.get_listing_by_id(listing_id=listing_id, db_session=db_session)
        if not listing:
            response_data = {"error": "Listing not found"}
            logger.error(msg=f"Listing: {listing_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Listing found", "listing": listing}
        logger.info(msg=f"Listing: {listing_id} found")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def create_listing(data: dict, db_session=None):
        """
        Creates a new listing with the provided data.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the success message and newly created listing ID, or a 400 error if the title is missing.
        """
        listing_data = data.get("listing", {})
        listing_data.update(user_id=current_user.id, status="active")

        listing_id = ListingMapper.create_listing(data=listing_data, db_session=db_session)
        if not listing_id:
            response_data = {"error": "Error creating listing"}
            logger.error(msg=f"Failed creating listing with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Listing created", "listing_id": listing_id}
        logger.info(msg=f"Listing: {listing_id} created successfully with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")
        

    @staticmethod
    def update_listing(listing_id: int, data: dict, db_session=None):
        """
        Updates an existing listing by its ID with the provided data.

        Args:
            listing_id: The ID of the listing to update.
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with a success message if the listing was updated, or a 404 error if the listing was not found.
        """
        updated_rows = ListingMapper.update_listing(listing_id=listing_id, data=data, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Error updating listing"}
            logger.error(msg=f"Failed updating listing: {listing_id} with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Listing updated", "updated_rows": updated_rows}
        logger.info(msg=f"Listing: {listing_id} updated successfully with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def delete_listing(listing_id: int, db_session=None):
        """
        Deletes a listing by its ID.

        Args:
            listing_id: The ID of the listing to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with a success message if the listing was deleted, or a 404 error if the listing was not found.
        """
        deleted_rows = ListingMapper.delete_listing(listing_id=listing_id, db_session=db_session)
        if not deleted_rows:
            response_data = {"message": "Listing not found"}
            logger.error(msg=f"Listing: {listing_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Listing deleted", "deleted_rows": deleted_rows}
        logger.info(msg=f"Listing: {listing_id} deleted successfully")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

