from flask import jsonify, Response
from flask_login import current_user

from ..data_mappers import ReviewMapper
from ..utils.logger import setup_logger

review_logger = setup_logger("review", "logs/review.log")


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

        if not reviews:
            response_data = {"error": "No reviews found"}
            review_logger.error("Data " + args + " was invalid and submitted by user " + current_user.id + ". No reviews found.")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Reviews found", "reviews": reviews}
        review_logger.info("Successfully got all reviews. " + reviews + ". User ID: " + current_user.id)
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")
            

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

        if not review:
            response_data = {"error": "Review not found"}
            review_logger.error("Data " + review_id + " was invalid and submitted by user " + current_user.id + ". Review not found.")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Review found", "review": review}
        review_logger.info("Review " + review_id + " was found by user " + current_user.id + ". Data: " + review)
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



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
        review_id = ReviewMapper.create_review(data=data, db_session=db_session)

        if not review_id:
            response_data = {"error": "Error creating review"}
            review_logger.error("Data " + data + " was invalid and submitted by user " + current_user.id + ". Failed to create review.")
            return Response(response=jsonify(response_data).get_data(), status=409, mimetype="application/json")

        response_data = {"message": "Review created", "review_id": review_id}
        review_logger.info("Review " + review_id + " was successfully created by user " + current_user.id)
        return Response(response=jsonify(response_data).get_data(), status=201, mimetype="application/json")
            

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

        if not updated_rows:
            response_data = {"error": "Review not found"}
            review_logger.error("Data " + data + " was invalid and submitted by user " + current_user.id + ". No review found.")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Review updated", "updated_rows": updated_rows}
        review_logger.info("Review with id " + review_id + " was successfully updated by user " + current_user.id + ". Contents: " + updated_rows)
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")



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

        if not deleted_rows:
            response_data = {"error": "Review not found"}
            review_logger.error("Data " + review_id + " was invalid and submitted by user " + current_user.id + ". No review found.")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        response_data = {"message": "Review deleted", "deleted_rows": deleted_rows}
        review_logger.info("Review with id " + review_id + " was successfully deleted by user " + current_user.id + ". Contents: " + deleted_rows)
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

