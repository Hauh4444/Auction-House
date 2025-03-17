import pytest
from datetime import datetime, date

from app.entities import Profile


@pytest.fixture
def mock_db_session():
    session = MagicMock()
    return session


def test_profile_creation():
    profile = Profile(
        user_id=1,
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
        phone_number="555-1234",
        address="123 Main St",
        city="Indiana",
        state="PA",
        country="USA",
        profile_picture="encoded_picture_string",
        bio="This is a short bio",
        social_links={"twitter": "https://twitter.com/johndoe"},
        created_at=datetime(2024, 1, 1),
        updated_at=datetime(2024, 1, 5),
        profile_id=1
    )

    assert profile.user_id == 1
    assert profile.first_name == "John"
    assert profile.last_name == "Doe"
    assert profile.date_of_birth == date(1990, 1, 1)
    assert profile.phone_number == "555-1234"
    assert profile.address == "123 Main St"
    assert profile.city == "Indiana"
    assert profile.state == "PA"
    assert profile.country == "USA"
    assert profile.profile_picture == "encoded_picture_string"
    assert profile.bio == "This is a short bio"
    assert profile.social_links == {"twitter": "https://twitter.com/johndoe"}
    assert profile.created_at == datetime(2024, 1, 1)
    assert profile.updated_at == datetime(2024, 1, 5)
    assert profile.profile_id == 1

    assert isinstance(profile.user_id, int)
    assert isinstance(profile.first_name, str)
    assert isinstance(profile.last_name, str)
    assert isinstance(profile.date_of_birth, date)
    assert isinstance(profile.phone_number, str)
    assert isinstance(profile.address, str)
    assert isinstance(profile.city, str)
    assert isinstance(profile.state, str)
    assert isinstance(profile.country, str)
    assert isinstance(profile.profile_picture, str)
    assert isinstance(profile.bio, str)
    assert isinstance(profile.social_links, dict)
    assert isinstance(profile.created_at, datetime)
    assert isinstance(profile.updated_at, datetime)
