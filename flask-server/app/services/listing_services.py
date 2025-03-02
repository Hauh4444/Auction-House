from flask import jsonify

from ..data_mappers import ListingMapper


class ListingService:
    @staticmethod
    def get_all_listings(args, db_session=None):
        """
        Retrieves a list of all listings, with optional filtering and sorting based on query parameters.

        Args:
            args (dict): Dictionary of query parameters.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response containing the list of listings with a 200 status code.
        """
        listings = ListingMapper.get_all_listings(args=args, db_session=db_session)
        return jsonify(listings), 200

    @staticmethod
    def get_listing_by_id(listing_id, db_session=None):
        """
        Retrieves a specific listing by its ID.

        Args:
            listing_id: The ID of the listing to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with the listing data if found, otherwise a 404 error with a message.
        """
        listing = ListingMapper.get_listing_by_id(listing_id=listing_id, db_session=db_session)
        if listing:
            return jsonify(listing), 200
        return jsonify({"error": "Listing not found"}), 404

    @staticmethod
    def create_listing(data, db_session=None):
        """
        Creates a new listing with the provided data.

        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with the success message and newly created listing ID, or a 400 error if the title is missing.
        """
        if not data.get("title"):
            return jsonify({"error": "Listing title is required"}), 400
        listing_id = ListingMapper.create_listing(data=data, db_session=db_session)
        return jsonify({"message": "Listing created", "listing_id": listing_id}), 201

    @staticmethod
    def update_listing(listing_id, data, db_session=None):
        """
        Updates an existing listing by its ID with the provided data.

        Args:
            listing_id: The ID of the listing to update.
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with a success message if the listing was updated, or a 404 error if the listing was not found.
        """
        updated_rows = ListingMapper.update_listing(listing_id=listing_id, data=data, db_session=db_session)
        if updated_rows:
            return jsonify({"message": "Listing updated"}), 200
        return jsonify({"error": "Listing not found"}), 404

    @staticmethod
    def delete_listing(listing_id, db_session=None):
        """
        Deletes a listing by its ID.

        Args:
            listing_id: The ID of the listing to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with a success message if the listing was deleted, or a 404 error if the listing was not found.
        """
        deleted_rows = ListingMapper.delete_listing(listing_id=listing_id, db_session=db_session)
        if deleted_rows:
            return jsonify({"message": "Listing deleted"}), 200
        return jsonify({"error": "Listing not found"}), 404
