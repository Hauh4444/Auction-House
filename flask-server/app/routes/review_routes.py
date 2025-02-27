from flask import Blueprint, request
from flask_login import login_required

from ..services.review_services import ReviewService

# Blueprint for review-related routes
review_bp = Blueprint('review_bp', __name__)


# GET /api/reviews
@review_bp.route('/', methods=['GET'])
def get_all_reviews(db_session=None):
    """Retrieve all reviews.

    Args:
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing a list of all reviews.
    """
    args = request.args
    return ReviewService.get_all_reviews(args=args, db_session=db_session)


# GET /api/reviews/{id}
@review_bp.route('/<int:review_id>', methods=['GET'])
def get_review(review_id, db_session=None):
    """Retrieve a single review by its ID.

    Args:
        review_id (int): The ID of the review to retrieve.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response containing review details.
    """
    return ReviewService.get_review_by_id(review_id=review_id, db_session=db_session)


# POST /api/reviews
@review_bp.route('/', methods=['POST'])
@login_required
def create_review(db_session=None):
    """Create a new review.

    Args:
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload with review details.

    Returns:
        JSON response containing the created review.
    """
    data = request.json
    return ReviewService.create_review(data=data, db_session=db_session)


# PUT /api/reviews/{id}
@review_bp.route('/<int:review_id>', methods=['PUT'])
@login_required
def update_review(review_id, db_session=None):
    """Update an existing review by its ID.

    Args:
        review_id (int): The ID of the review to update.
        db_session: Optional database session to be used in tests.

    Expects:
        JSON payload with updated review details.

    Returns:
        JSON response containing the updated review.
    """
    data = request.json
    return ReviewService.update_review(review_id=review_id, data=data, db_session=db_session)


# DELETE /api/reviews/{id}
@review_bp.route('/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id, db_session=None):
    """Delete a review by its ID.

    Args:
        review_id (int): The ID of the review to delete.
        db_session: Optional database session to be used in tests.

    Returns:
        JSON response indicating the deletion status.
    """
    return ReviewService.delete_review(review_id=review_id, db_session=db_session)
