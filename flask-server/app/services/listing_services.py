from flask import jsonify, Response, session

from ..data_mappers import ListingMapper
from ..utils.logger import setup_logger

listings_logger = setup_logger("listings", "logs/listings.log")


class ListingService:
    @staticmethod
    def get_all_listings(args, db_session=None):
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
            listings_logger.error("Error: No listings found.")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Listings found", "listings": listings}
        listings_logger.info("Listings found by user " + session.get("user_id") + " and contains: " + listings)
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")
        

    @staticmethod
    def get_listing_by_id(listing_id, db_session=None):
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
            listings_logger.error("Listing not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Listing found", "listing": listing}
        listings_logger.info("Listing found by user " + session.get("user_id") + " and contains: " + listing)
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def create_listing(data, db_session=None):
        """
        Creates a new listing with the provided data.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the success message and newly created listing ID, or a 400 error if the title is missing.
        """
        listing_data = data.get("listing", {})
        listing_data.update(user_id=session.get("user_id"), status="active")

        listing_id = ListingMapper.create_listing(data=listing_data, db_session=db_session)

        if not listing_id:
            response_data = {"error": "Error creating listing"}
            listings_logger.error("Error creating listing")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Listing created", "listing_id": listing_id}
        listings_logger.info("Listing created by " + session.get("user_id") + ". Listing ID: " + listing_id)
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")
        

    @staticmethod
    def update_listing(listing_id, data, db_session=None):
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
            response_data = {"error": "Listing not found"}
            listings_logger.error("Failed to update listing. Listing not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Listing updated", "updated_rows": updated_rows}
        listings_logger.info("Listing updated by " + session.get("user_id") + ". Updated data: " + updated_rows)
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def delete_listing(listing_id, db_session=None):
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
            listings_logger.error("Error deleting listing. Listing not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Listing deleted", "deleted_rows": deleted_rows}
        listings_logger.info("Listing deleted by " + session.get("user_id") + ". Deleted data: " + deleted_rows)
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

