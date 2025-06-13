from flask import jsonify, Response

from ..data_mappers import ReviewMapper
from ..utils.logger import setup_logger

logger = setup_logger(name="review_logger", log_file="logs/review.log")

class ReviewService:
    @staticmethod
    def get_all_reviews(args: dict, db_session=None):
        """
        Retrieves a list of all reviews.

        Args:
            args (dict): Dictionary of query parameters.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object containing the list of reviews with a 200 status code.
        """
        reviews = ReviewMapper.get_all_reviews(args=args, db_session=db_session)
        if not reviews:
            response_data = {"error": "No reviews found"}
            logger.error(msg=f"No reviews found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Reviews found", "reviews": reviews}
        logger.info(msg=f"Reviews found: {[review.get('title') for review in reviews]}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")
            

    @staticmethod
    def get_review_by_id(review_id: int, db_session=None):
        """
        Retrieves a specific review by its ID.
        
        Args:
            review_id: The ID of the review to retrieve.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the review data if found, otherwise a 404 error with a message.
        """
        review = ReviewMapper.get_review_by_id(review_id=review_id, db_session=db_session)
        if not review:
            response_data = {"error": "Review not found"}
            logger.error(msg=f"Review: {review_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Review found", "review": review}
        logger.info(msg=f"Review: {review_id} found")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def create_review(data: dict, db_session=None):
        """
        Creates a new review with the provided data.
        
        Args:
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with the success message and newly created reviewID,
            or a 400 error if required fields are missing.
        """
        review_id = ReviewMapper.create_review(data=data, db_session=db_session)
        if not review_id:
            response_data = {"error": "Error creating review"}
            logger.error(msg=f"Failed creating review with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Review created", "review_id": review_id}
        logger.info(msg=f"Review: {review_id} created successfully with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")
            

    @staticmethod
    def update_review(review_id: int, data: dict, db_session=None):
        """
        Updates an existing review by its ID with the provided data.
        
        Args:
            review_id: The ID of the review to update.
            data: A dictionary containing the request arguments.
            db_session: Optional database session to be used in tests.

        Returns:
            A Response object with a success message if the review was updated,
            or a 409 error if the review was not updated.
        """
        updated_rows = ReviewMapper.update_review(review_id=review_id, data=data, db_session=db_session)
        if not updated_rows:
            response_data = {"error": "Error updating review"}
            logger.error(msg=f"Failed updating review: {review_id} with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Review updated", "updated_rows": updated_rows}
        logger.info(msg=f"Review: {review_id} updated successfully with data: {', '.join(f'{k}={v!r}' for k, v in data.items())}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



    @staticmethod
    def delete_review(review_id: int, db_session=None):
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
        if not deleted_rows:
            response_data = {"error": "Review not found"}
            logger.error(msg=f"Review: {review_id} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Review deleted", "deleted_rows": deleted_rows}
        logger.info(msg=f"Review: {review_id} deleted successfully")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

