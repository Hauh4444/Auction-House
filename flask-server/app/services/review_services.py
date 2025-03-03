from flask import jsonify, Response

from ..data_mappers import ReviewMapper


class ReviewService:
    @staticmethod
    def get_all_reviews(args, db_session=None):
        """
        Retrieves a list of all reviews.

        Args:
            args (dict): Dictionary of query parameters.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object containing the list of reviews with a 200 status code.
        """
        reviews = ReviewMapper.get_all_reviews(args=args, db_session=db_session)
        data = {"message": "Reviews found", "reviews": reviews}
        response = Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
        return response
    
    @staticmethod
    def get_review_by_id(review_id, db_session=None):
        """
        Retrieves a specific review by its ID.
        
        Args:
            review_id: The ID of the review to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the review data if found, otherwise a 404 error with a message.
        """
        review = ReviewMapper.get_review_by_id(review_id=review_id, db_session=db_session)

        if review:
            data = {"message": "Review found", "review": review}
            response = Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
            return response

        data = {"message": "Review not found"}
        response = Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')
        return response
    
    @staticmethod
    def create_review(data, db_session=None):
        """
        Creates a new review with the provided data.
        
        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the success message and newly created reviewID,
            or a 400 error if required fields are missing.
        """
        required_fields = ["listing_id", "user_id", "username", "title", "description", "stars", "created_at"]

        if not all(field in data for field in required_fields):
            data = {"error": "Required fields are missing"}
            response = Response(response=jsonify(data).get_data(), status=400, mimetype='application/json')
            return response
        
        review_id = ReviewMapper.create_review(data=data, db_session=db_session)

        data = {"message": "Review created", "review_id": review_id}
        response = Response(response=jsonify(data).get_data(), status=201, mimetype='application/json')
        return response
    
    @staticmethod
    def update_review(review_id, data, db_session=None):
        """
        Updates an existing review by its ID with the provided data.
        
        Args:
            review_id: The ID of the review to update.
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with a success message if the review was updated,
            or a 404 error if the review was not found.
        """
        updated_rows = ReviewMapper.update_review(review_id=review_id, data=data, db_session=db_session)

        if updated_rows:
            data = {"message": "Review updated", "updated_rows": updated_rows}
            response = Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
            return response

        data = {"error": "Review not found"}
        response = Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')
        return response
    
    @staticmethod
    def delete_review(review_id, db_session=None):
        """
        Deletes a review by its ID.
        
        Args:
            review_id: The ID of the review to delete.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with a success message if the review was deleted,
            or a 404 error if the review was not found.
            """
        deleted_rows = ReviewMapper.delete_review(review_id=review_id, db_session=db_session)

        if deleted_rows:
            data = {"message": "Review deleted", "deleted_rows": deleted_rows}
            response = Response(response=jsonify(data).get_data(), status=200, mimetype='application/json')
            return response

        data = {"error": "Review not found"}
        response = Response(response=jsonify(data).get_data(), status=404, mimetype='application/json')
        return response