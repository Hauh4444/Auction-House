import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.entities import Listing


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
    assert isinstance(listing.user_id, int)
    assert isinstance(listing.category_id, int)
    assert isinstance(listing.title, str)
    assert isinstance(listing.title_short, str)
    assert isinstance(listing.description, str)
    assert isinstance(listing.item_specifics, str)
    assert isinstance(listing.listing_type, str)
    assert isinstance(listing.buy_now_price, (int, float))
    assert isinstance(listing.status, str)
    assert isinstance(listing.image_encoded, str)
    assert isinstance(listing.created_at, datetime)
    assert isinstance(listing.updated_at, datetime)


def test_listing_with_optional_fields():
    listing = Listing(
        listing_id=1,
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
        updated_at=datetime(2024, 1, 1, 12, 0, 0)
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
    assert isinstance(listing.listing_id, int)
    assert isinstance(listing.starting_price, (int, float))
    assert isinstance(listing.reserve_price, (int, float))
    assert isinstance(listing.current_price, (int, float))
    assert isinstance(listing.auction_start, datetime)
    assert isinstance(listing.auction_end, datetime)
    assert isinstance(listing.bids, int)
    assert isinstance(listing.purchases, int)
    assert isinstance(listing.average_review, (int, float))
    assert isinstance(listing.total_reviews, int)
    assert isinstance(listing.created_at, datetime)
    assert isinstance(listing.updated_at, datetime)


def test_listing_to_dict():
    listing = Listing(
        listing_id=1,
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
        updated_at=datetime(2024, 1, 1, 12, 0, 0)
    )

    listing_dict = listing.to_dict()

    assert listing_dict["listing_id"] == 1
    assert listing_dict["starting_price"] == 300.00
    assert listing_dict["reserve_price"] == 450.00
    assert listing_dict["current_price"] == 350.00
    assert listing_dict["auction_start"] == datetime(2024, 1, 1, 10, 0, 0)
    assert listing_dict["auction_end"] == datetime(2024, 1, 1, 18, 0, 0)
    assert listing_dict["bids"] == 5
    assert listing_dict["purchases"] == 2
    assert listing_dict["average_review"] == 4.5
    assert listing_dict["total_reviews"] == 50
    assert listing_dict["created_at"] == datetime(2024, 1, 1, 10, 0, 0) 
    assert listing_dict["updated_at"] == datetime(2024, 1, 1, 12, 0, 0)
    assert isinstance(listing_dict["listing_id"], int)
    assert isinstance(listing_dict["starting_price"], (int, float))
    assert isinstance(listing_dict["reserve_price"], (int, float))
    assert isinstance(listing_dict["current_price"], (int, float))
    assert isinstance(listing_dict["auction_start"], datetime)
    assert isinstance(listing_dict["auction_end"], datetime)
    assert isinstance(listing_dict["bids"], int)
    assert isinstance(listing_dict["purchases"], int)
    assert isinstance(listing_dict["average_review"], (int, float))
    assert isinstance(listing_dict["total_reviews"], int)
    assert isinstance(listing_dict["created_at"], datetime)
    assert isinstance(listing_dict["updated_at"], datetime)


# noinspection PyArgumentList
def test_listing_missing_required_fields():
    with pytest.raises(expected_exception=TypeError):
        Listing()


# noinspection PyTypeChecker
def test_listing_invalid_types():
    with pytest.raises(expected_exception=TypeError):
        Listing(
            listing_id="1",
            user_id="1",
            category_id="2",
            title=1,
            title_short=1,
            description=1,
            item_specifics=1,
            listing_type=1,
            buy_now_price="500.00",
            starting_price="300.00",
            reserve_price="450.00",
            current_price="350.00",
            auction_start=1,
            auction_end=1,
            bids="5",
            purchases="2",
            average_review="4.5",
            total_reviews="50",
            status=1,
            image_encoded=1,
            created_at=1,
            updated_at=1
        )

    with pytest.raises(expected_exception=ValueError):
        Listing(
            user_id=1,
            category_id=2,
            title="Smartphone",
            title_short="Smartphone",
            description="Latest model smartphone",
            item_specifics="Brand: ABC, Color: Black, Condition: New",
            listing_type="invalid_type",
            buy_now_price=500.00,
            status="invalid_type",
            image_encoded="image_data"
        )
