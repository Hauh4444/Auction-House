from flask import jsonify
from ..data_mappers.listings import ListingMapper


class ListingService:
    @staticmethod
    def get_all_listings(request):
        """
        Retrieves a list of all listings, with optional filtering and sorting based on query parameters.

        Args:
            request: The request object containing query parameters for filtering, sorting, and pagination.

        Returns:
            A JSON response containing the list of listings with a 200 status code.
        """
        listings = ListingMapper.get_all_listings(args=request.args)
        return jsonify(listings), 200

    @staticmethod
    def get_listing_by_id(listing_id):
        """
        Retrieves a specific listing by its ID.

        Args:
            listing_id: The ID of the listing to retrieve.

        Returns:
            A JSON response with the listing data if found, otherwise a 404 error with a message.
        """
        listing = ListingMapper.get_listing_by_id(listing_id)
        if listing:
            return jsonify(listing), 200
        return jsonify({"error": "Listing not found"}), 404

    @staticmethod
    def create_listing(data):
        """
        Creates a new listing with the provided data.

        Args:
            data: A dictionary containing the listing details such as title, description, price, etc.

        Returns:
            A JSON response with the success message and newly created listing ID, or a 400 error if the title is missing.
        """
        if not data.get("title"):
            return jsonify({"error": "Listing title is required"}), 400
        listing_id = ListingMapper.create_listing(data)
        return jsonify({"message": "Listing created", "listing_id": listing_id}), 201

    @staticmethod
    def update_listing(listing_id, data):
        """
        Updates an existing listing by its ID with the provided data.

        Args:
            listing_id: The ID of the listing to update.
            data: A dictionary containing the fields to update.

        Returns:
            A JSON response with a success message if the listing was updated, or a 404 error if the listing was not found.
        """
        updated_rows = ListingMapper.update_listing(listing_id, data)
        if updated_rows:
            return jsonify({"message": "Listing updated"}), 200
        return jsonify({"error": "Listing not found"}), 404

    @staticmethod
    def delete_listing(listing_id):
        """
        Deletes a listing by its ID.

        Args:
            listing_id: The ID of the listing to delete.

        Returns:
            A JSON response with a success message if the listing was deleted, or a 404 error if the listing was not found.
        """
        deleted_rows = ListingMapper.delete_listing(listing_id)
        if deleted_rows:
            return jsonify({"message": "Listing deleted"}), 200
        return jsonify({"error": "Listing not found"}), 404
