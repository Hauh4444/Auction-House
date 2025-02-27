import pytest
from unittest.mock import MagicMock
from app.data_mappers.listing_mapper import ListingMapper


# Fixture for a mock database session
@pytest.fixture
def mock_db_session():
    session = MagicMock()
    # Mock the cursor and its behavior
    cursor = MagicMock()
    session.cursor.return_value = cursor
    return session


def test_get_listing(mock_db_session):
    # Mock the cursor's execute and fetchone behavior
    mock_cursor = mock_db_session.cursor.return_value
    mock_cursor.fetchone.return_value = {
        'listing_id': 1,
        'user_id': 1,
        'title': "AK45 Stereo Audio Amplifier,300W Home 2 Channel Wireless Bluetooth 5.0 Power Amplifier System",
        'title_short': "AK45 Stereo Amplifier",
        'description': "",
        'item_specifics': "",
        'category_id': 5,
        'listing_type': "buy_now",
        'starting_price': 37.04,
        'buy_now_price': 37.04,
        'status': "active",
        'image_encoded': "j"
    }

    # Call the method you are testing
    listing = ListingMapper.get_listing_by_id(listing_id=18, db_session=mock_db_session)

    assert listing is not None
    assert listing["listing_id"] == 1
    assert listing["title"] == "AK45 Stereo Audio Amplifier,300W Home 2 Channel Wireless Bluetooth 5.0 Power Amplifier System"
    assert listing["category_id"] == 5
    assert listing["starting_price"] == 37.04
