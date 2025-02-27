import pytest
from unittest.mock import MagicMock
from datetime import datetime

from app.data_mappers.listing_mapper import ListingMapper


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    session.cursor.return_value = session
    return session


def test_get_all_listings(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = [
        {
            "listing_id": 1, "user_id": 10, "category_id": 2, "title": "Laptop", "title_short": "Gaming Laptop",
            "description": "Gaming laptop with RTX 3060", "item_specifics": "16GB RAM, 512GB SSD",
            "listing_type": "auction", "status": "active", "image_encoded": "image_data", "buy_now_price": 1200, 
            "starting_price": 1000, "reserve_price": 1100, "current_price": 1050, 
            "auction_start": datetime(2024, 1, 1), "auction_end": datetime(2024, 1, 7),
            "bids": 5, "purchases": 0, "average_review": 4.5, "total_reviews": 10,
            "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 2)
        },
        {
            "listing_id": 2, "user_id": 10, "category_id": 2, "title": "Laptop", "title_short": "Gaming Laptop",
            "description": "Gaming laptop with RTX 3060", "item_specifics": "16GB RAM, 512GB SSD",
            "listing_type": "auction", "status": "active", "image_encoded": "image_data", "buy_now_price": 1200, 
            "starting_price": 1000, "reserve_price": 1100, "current_price": 1050, 
            "auction_start": datetime(2024, 1, 1), "auction_end": datetime(2024, 1, 7),
            "bids": 5, "purchases": 0, "average_review": 4.5, "total_reviews": 10,
            "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 2)
        }
    ]
    args = {"min_price": 500}

    listings = ListingMapper.get_all_listings(args, mock_db_session)

    assert len(listings) == 2
    assert listings[0]["title"] == "Laptop"


def test_get_listing_by_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
            "listing_id": 1, "user_id": 10, "category_id": 2, "title": "Laptop", "title_short": "Gaming Laptop",
            "description": "Gaming laptop with RTX 3060", "item_specifics": "16GB RAM, 512GB SSD",
            "listing_type": "auction", "status": "active", "image_encoded": "image_data", "buy_now_price": 1200, 
            "starting_price": 1000, "reserve_price": 1100, "current_price": 1050, 
            "auction_start": datetime(2024, 1, 1), "auction_end": datetime(2024, 1, 7),
            "bids": 5, "purchases": 0, "average_review": 4.5, "total_reviews": 10,
            "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 2)
    }

    listing = ListingMapper.get_listing_by_id(1, mock_db_session)

    assert listing["listing_id"] == 1
    assert listing["title"] == "Laptop"


def test_create_listing(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
            "listing_id": 1, "user_id": 10, "category_id": 2, "title": "Laptop", "title_short": "Gaming Laptop",
            "description": "Gaming laptop with RTX 3060", "item_specifics": "16GB RAM, 512GB SSD",
            "listing_type": "auction", "status": "active", "image_encoded": "image_data", "buy_now_price": 1200, 
            "starting_price": 1000, "reserve_price": 1100, "current_price": 1050, 
            "auction_start": datetime(2024, 1, 1), "auction_end": datetime(2024, 1, 7),
            "bids": 5, "purchases": 0, "average_review": 4.5, "total_reviews": 10,
            "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 2)
    }

    listing_id = ListingMapper.create_listing(data, mock_db_session)

    assert listing_id == 3


def test_update_listing(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1
    data = {
        "title": "Updated Laptop",
        "buy_now_price": 1300
    }

    rows_updated = ListingMapper.update_listing(1, data, mock_db_session)

    assert rows_updated == 1


def test_delete_listing(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 1

    rows_deleted = ListingMapper.delete_listing(1, mock_db_session)

    assert rows_deleted == 1


def test_create_listing_missing_fields(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
            "listing_id": 1, "user_id": 10, "category_id": 2, "title": "Laptop", "title_short": "Gaming Laptop",
            "description": "Gaming laptop with RTX 3060", "item_specifics": "16GB RAM, 512GB SSD",
            "listing_type": "auction", "status": "active", "image_encoded": "image_data", "buy_now_price": 1200, 
            "starting_price": 1000, "reserve_price": 1100, "current_price": 1050, 
            "auction_start": datetime(2024, 1, 1), "auction_end": datetime(2024, 1, 7),
            "bids": 5, "purchases": 0, "average_review": 4.5, "total_reviews": 10,
            "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 2)
    }

    del data["title"]

    with pytest.raises(TypeError):
        ListingMapper.create_listing(data, mock_db_session)


def test_create_listing_invalid_data_type(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.lastrowid = 3
    data = {
            "listing_id": 1, "user_id": 10, "category_id": 2, "title": "Laptop", "title_short": "Gaming Laptop",
            "description": "Gaming laptop with RTX 3060", "item_specifics": "16GB RAM, 512GB SSD",
            "listing_type": "auction", "status": "active", "image_encoded": "image_data", "buy_now_price": 1200, 
            "starting_price": 1000, "reserve_price": 1100, "current_price": 1050, 
            "auction_start": datetime(2024, 1, 1), "auction_end": datetime(2024, 1, 7),
            "bids": 5, "purchases": 0, "average_review": 4.5, "total_reviews": 10,
            "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 2)
    }
    
    # Invalid type for created_at, should be datetime
    data["created_at"] = 2023

    with pytest.raises(TypeError):
        ListingMapper.create_listing(data, mock_db_session)


def test_get_listing_by_id_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        ListingMapper.get_listing_by_id(1, mock_db_session)


def test_get_all_listings_no_results(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchall.return_value = []

    listings = ListingMapper.get_all_listings({}, mock_db_session)

    assert len(listings) == 0


def test_create_listing_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    data = {
            "listing_id": 1, "user_id": 10, "category_id": 2, "title": "Laptop", "title_short": "Gaming Laptop",
            "description": "Gaming laptop with RTX 3060", "item_specifics": "16GB RAM, 512GB SSD",
            "listing_type": "auction", "status": "active", "image_encoded": "image_data", "buy_now_price": 1200, 
            "starting_price": 1000, "reserve_price": 1100, "current_price": 1050, 
            "auction_start": datetime(2024, 1, 1), "auction_end": datetime(2024, 1, 7),
            "bids": 5, "purchases": 0, "average_review": 4.5, "total_reviews": 10,
            "created_at": datetime(2024, 1, 1), "updated_at": datetime(2024, 1, 2)
    }

    with pytest.raises(Exception, match="Database error"):
        ListingMapper.create_listing(data, mock_db_session)


def test_update_listing_invalid_id(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.rowcount = 0  # Simulate no rows were updated

    data = {
        "title": "Updated Laptop",
        "buy_now_price": 1300
    }

    rows_updated = ListingMapper.update_listing(999, data, mock_db_session)  # Invalid ID

    assert rows_updated == 0  # Expecting no rows to be updated


def test_delete_listing_db_failure(mock_db_session):
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        ListingMapper.delete_listing(1, mock_db_session)

