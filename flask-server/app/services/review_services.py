from flask import jsonify
from ..data_mappers.review_mapper import ReviewMapper

class ReviewService:
    @staticmethod
    def get_all_reviews(args, db_session=None):
        """
        Retrieves a list of all reviews.

        Args:
            args (dict): Dictionary of query parameters.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response containing the list of reviews with a 200 status code.
        """
        reviews = ReviewMapper.get_all_reviews(args, db_session=db_session)
        return jsonify(reviews), 200
    
    @staticmethod
    def get_review_by_id(review_id, db_session=None):
        """
        Retrieves a specific review by its ID.
        
        Args:
            review_id: The ID of the review to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with the review data if found, otherwise a 404 error with a message.
        """
        review = ReviewMapper.get_review_by_id(review_id, db_session=db_session)
        if review:
            return jsonify(review), 200
        return jsonify({"error": "Review not found"}), 404
    
    @staticmethod
    def create_review(data, db_session=None):
        """
        Creates a new review with the provided data.
        
        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with the success message and newly created reviewID,
            or a 400 error if required fields are missing.
        """
        required_fields = ["listing_id", "user_id", "username", "title", "description", "stars", "created_at"]
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Missing required review fields"}), 400
        
        review_id = ReviewMapper.create_review(data, db_session=db_session)
        return jsonify({"message": "Review created", "review_id": review_id}), 201
    
    @staticmethod
    def update_review(review_id, data, db_session=None):
        """
        Updates an existing review by its ID with the provided data.
        
        Args:
            review_id: The ID of the review to update.
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with a success message if the review was updated,
            or a 404 error if the review was not found.
        """
        updated_rows = ReviewMapper.update_review(review_id, data, db_session=db_session)
        if updated_rows:
            return jsonify({"message": "Review updated"}), 200
        return jsonify({"error": "Review not found"}), 404
    
    @staticmethod
    def delete_review(review_id, db_session=None):
        """
        Deletes a review by its ID.
        
        Args:
            review_id: The ID of the review to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            A JSON response with a success message if the review was deleted,
            or a 404 error if the review was not found.
            """
        deleted_rows = ReviewMapper.delete_review(review_id, db_session=db_session)
        if deleted_rows:
            return jsonify({"message": "Review deleted"}), 200
        return jsonify({"error": "Review not found"}), 404