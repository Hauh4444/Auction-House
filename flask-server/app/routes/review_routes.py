from flask import Blueprint, request

from ..services.reviews import ReviewService

# Blueprint for review-related routes
review_bp = Blueprint('review_bp', __name__)


# GET /api/reviews
@review_bp.route('/', methods=['GET'])
def get_all_reviews():
    """Retrieve all reviews.

    Returns:
        JSON response containing a list of all reviews.
    """
    return ReviewService.get_all_reviews()


# GET /api/reviews/{id}
@review_bp.route('/<int:review_id>', methods=['GET'])
def get_review(review_id):
    """Retrieve a single review by its ID.

    Args:
        review_id (int): The ID of the review to retrieve.

    Returns:
        JSON response containing review details.
    """
    return ReviewService.get_review_by_id(review_id)


# POST /api/reviews
@review_bp.route('/', methods=['POST'])
def create_review():
    """Create a new review.

    Expects:
        JSON payload with review details.

    Returns:
        JSON response containing the created review.
    """
    data = request.json
    return ReviewService.create_review(data)


# PUT /api/reviews/{id}
@review_bp.route('/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    """Update an existing review by its ID.

    Args:
        review_id (int): The ID of the review to update.

    Expects:
        JSON payload with updated review details.

    Returns:
        JSON response containing the updated review.
    """
    data = request.json
    return ReviewService.update_review(review_id, data)


# DELETE /api/reviews/{id}
@review_bp.route('/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review by its ID.

    Args:
        review_id (int): The ID of the review to delete.

    Returns:
        JSON response indicating the deletion status.
    """
    return ReviewService.delete_review(review_id)
