from flask import jsonify, Response

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
            A Response object containing the list of listings with a 200 status code.
        """
        listings = ListingMapper.get_all_listings(args=args, db_session=db_session)

        if not listings:
            data = {"message": "No listings found"}
            return Response(response=jsonify(data).get_data(), status=404, mimetype="application/json")

        data = {"message": "Listings found", "listings": listings}
        return Response(response=jsonify(data).get_data(), status=200, mimetype="application/json")
        

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
            data = {"error": "Listing not found"}
            return Response(response=jsonify(data).get_data(), status=404, mimetype="application/json")

        data = {"message": "Listing found", "listing": listing}
        return Response(response=jsonify(data).get_data(), status=200, mimetype="application/json")



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
        listing_id = ListingMapper.create_listing(data=data, db_session=db_session)

        if not listing_id:
            data = {"message": "Error creating listing"}
            return Response(response=jsonify(data).get_data(), status=400, mimetype="application/json")

        data = {"message": "Listing created", "listing_id": listing_id}
        return Response(response=jsonify(data).get_data(), status=201, mimetype="application/json")
        

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
            data = {"error": "Listing not found"}
            return Response(response=jsonify(data).get_data(), status=404, mimetype="application/json")

        data = {"message": "Listing updated", "updated_rows": updated_rows}
        return Response(response=jsonify(data).get_data(), status=200, mimetype="application/json")



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
            data = {"message": "Listing not found"}
            return Response(response=jsonify(data).get_data(), status=404, mimetype="application/json")

        data = {"message": "Listing deleted", "deleted_rows": deleted_rows}
        return Response(response=jsonify(data).get_data(), status=200, mimetype="application/json")

