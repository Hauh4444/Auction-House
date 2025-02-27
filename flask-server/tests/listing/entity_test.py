import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.entities.listing import Listing


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session


def test_listing_creation():
    listing = Listing(
        user_id=1,
        category_id=2,
        title="Smartphone",
        title_short="Smartphone",
        description="Latest model smartphone",
        item_specifics="Brand: ABC, Color: Black, Condition: New",
        listing_type="buy_now",
        buy_now_price=500.00,
        status="active",
        image_encoded="image_data"
    )

    assert listing.user_id == 1
    assert listing.category_id == 2
    assert listing.title == "Smartphone"
    assert listing.title_short == "Smartphone"
    assert listing.description == "Latest model smartphone"
    assert listing.item_specifics == "Brand: ABC, Color: Black, Condition: New"
    assert listing.listing_type == "buy_now"
    assert listing.buy_now_price == 500.00
    assert listing.status == "active"
    assert listing.image_encoded == "image_data"
    assert isinstance(listing.created_at, str)
    assert isinstance(listing.updated_at, str)


def test_listing_with_optional_fields():
    listing = Listing(
        user_id=1,
        category_id=2,
        title="Smartphone",
        title_short="Smartphone",
        description="Latest model smartphone",
        item_specifics="Brand: ABC, Color: Black, Condition: New",
        listing_type="auction",
        buy_now_price=500.00,
        starting_price=300.00,
        reserve_price=450.00,
        current_price=350.00,
        auction_start=datetime(2024, 1, 1, 10, 0, 0),
        auction_end=datetime(2024, 1, 1, 18, 0, 0),
        bids=5,
        purchases=2,
        average_review=4.5,
        total_reviews=50,
        status="active",
        image_encoded="image_data",
        created_at=datetime(2024, 1, 1, 10, 0, 0),
        updated_at=datetime(2024, 1, 1, 12, 0, 0),
        listing_id=1
    )

    assert listing.listing_id == 1
    assert listing.starting_price == 300.00
    assert listing.reserve_price == 450.00
    assert listing.current_price == 350.00
    assert listing.auction_start == datetime(2024, 1, 1, 10, 0, 0)
    assert listing.auction_end == datetime(2024, 1, 1, 18, 0, 0)
    assert listing.bids == 5
    assert listing.purchases == 2
    assert listing.average_review == 4.5
    assert listing.total_reviews == 50
    assert listing.created_at == datetime(2024, 1, 1, 10, 0, 0)
    assert listing.updated_at == datetime(2024, 1, 1, 12, 0, 0)


def test_listing_to_dict():
    listing = Listing(
        user_id=1,
        category_id=2,
        title="Smartphone",
        title_short="Smartphone",
        description="Latest model smartphone",
        item_specifics="Brand: ABC, Color: Black, Condition: New",
        listing_type="buy_now",
        buy_now_price=500.00,
        status="active",
        image_encoded="image_data"
    )

    listing_dict = listing.to_dict()

    assert listing_dict["user_id"] == 1
    assert listing_dict["category_id"] == 2
    assert listing_dict["title"] == "Smartphone"
    assert listing_dict["title_short"] == "Smartphone"
    assert listing_dict["description"] == "Latest model smartphone"
    assert listing_dict["item_specifics"] == "Brand: ABC, Color: Black, Condition: New"
    assert listing_dict["listing_type"] == "buy_now"
    assert listing_dict["buy_now_price"] == 500.00
    assert listing_dict["status"] == "active"
    assert listing_dict["image_encoded"] == "image_data"
    assert isinstance(listing_dict["created_at"], str)
    assert isinstance(listing_dict["updated_at"], str)


def test_listing_missing_required_fields():
    with pytest.raises(TypeError):
        Listing()


def test_listing_invalid_types():
    with pytest.raises(TypeError):
        Listing(
            user_id="not_a_number",  # Invalid type
            category_id=2,
            title="Smartphone",
            title_short="Smartphone",
            description="Latest model smartphone",
            item_specifics="Brand: ABC, Color: Black, Condition: New",
            listing_type="buy_now",
            buy_now_price=500.00,
            status="active",
            image_encoded="image_data"
        )

    with pytest.raises(ValueError):
        Listing(
            user_id=1,
            category_id=2,
            title="Smartphone",
            title_short="Smartphone",
            description="Latest model smartphone",
            item_specifics="Brand: ABC, Color: Black, Condition: New",
            listing_type="invalid_type",  # Invalid listing_type
            buy_now_price=500.00,
            status="active",
            image_encoded="image_data"
        )
