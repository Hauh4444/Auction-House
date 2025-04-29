import pytest
from datetime import datetime
from app.entities import Review

def test_review_creation():
    review = Review(
        listing_id=1,
        user_id=2,
        username="johndoe",
        title="Great product",
        description="I really liked this product. It works well!",
        stars=4.5
    )
    
    assert review.listing_id == 1
    assert review.user_id == 2
    assert review.username == "johndoe"
    assert review.title == "Great product"
    assert review.description == "I really liked this product. It works well!"
    assert review.stars == 4.5
    assert isinstance(review.created_at, str)

def test_review_with_optional_fields():
    review = Review(
        review_id=10,
        listing_id=3,
        user_id=5,
        username="janedoe",
        title="Not bad",
        description="The product is okay but could be improved.",
        stars=3.0,
        created_at=datetime(2024, 3, 18, 10, 0, 0)
    )
    
    assert review.review_id == 10
    assert review.created_at == datetime(2024, 3, 18, 10, 0, 0)

def test_review_to_dict():
    review = Review(
        review_id=7,
        listing_id=8,
        user_id=4,
        username="alice123",
        title="Excellent!",
        description="Highly recommend this product.",
        stars=5.0
    )
    
    review_dict = review.to_dict()
    
    assert review_dict["review_id"] == 7
    assert review_dict["listing_id"] == 8
    assert review_dict["user_id"] == 4
    assert review_dict["username"] == "alice123"
    assert review_dict["title"] == "Excellent!"
    assert review_dict["description"] == "Highly recommend this product."
    assert review_dict["stars"] == 5.0

def test_review_missing_required_fields():
    with pytest.raises(TypeError):
        Review()

def test_review_invalid_types():
    with pytest.raises(TypeError):
        Review(
            review_id="10",
            listing_id="3",
            user_id="5",
            username=123,
            title=456,
            description=789,
            stars="five"
        )
