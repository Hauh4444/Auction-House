import pytest
from unittest.mock import MagicMock
from ...app.entities.listing import Listing


# Fixture for a mock database session
@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session


# Test Listing Entity
def test_listing_entity():
    listing = Listing(
        user_id=1,
        title_short="AK45 Stereo Amplifier",
        description="",
        item_specifics="",
        listing_type="buy_now",
        buy_now_price=37.04,
        status="up",
        image_encoded="j",
        listing_id=18,
        title="AK45 Stereo Audio Amplifier,300W Home 2 Channel Wireless Bluetooth 5.0 Power Amplifier System",
        category_id=5,
        starting_price=37.04
    )
    assert listing.listing_id == 18
    assert listing.title == "AK45 Stereo Audio Amplifier,300W Home 2 Channel Wireless Bluetooth 5.0 Power Amplifier System"
    assert listing.category_id == 5
    assert listing.starting_price == 37.04