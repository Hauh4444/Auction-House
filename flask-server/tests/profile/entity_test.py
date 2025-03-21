import pytest
from datetime import datetime, date
from app.entities import Profile

def test_profile_creation():
    profile = Profile(
        user_id=1,
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 5, 15),
        phone_number="123-456-7890",
        address="123 Main St",
        city="Springfield",
        state="IL",
        country="USA"
    )
    
    assert profile.user_id == 1
    assert profile.first_name == "John"
    assert profile.last_name == "Doe"
    assert profile.date_of_birth == date(1990, 5, 15)
    assert profile.phone_number == "123-456-7890"
    assert profile.address == "123 Main St"
    assert profile.city == "Springfield"
    assert profile.state == "IL"
    assert profile.country == "USA"
    assert isinstance(profile.created_at, datetime)
    assert isinstance(profile.updated_at, datetime)

def test_profile_with_optional_fields():
    profile = Profile(
        profile_id=10,
        user_id=2,
        first_name="Jane",
        last_name="Smith",
        date_of_birth=date(1985, 8, 25),
        phone_number="987-654-3210",
        address="456 Oak St",
        city="Lincoln",
        state="NE",
        country="USA",
        profile_picture="encoded_string",
        bio="Loves coding",
        social_links={"twitter": "@janesmith"},
        created_at=datetime(2024, 3, 18, 10, 0, 0),
        updated_at=datetime(2024, 3, 18, 12, 0, 0)
    )
    
    assert profile.profile_id == 10
    assert profile.profile_picture == "encoded_string"
    assert profile.bio == "Loves coding"
    assert profile.social_links == {"twitter": "@janesmith"}
    assert isinstance(profile.created_at, datetime)
    assert isinstance(profile.updated_at, datetime)

def test_profile_to_dict():
    profile = Profile(
        profile_id=5,
        user_id=3,
        first_name="Alice",
        last_name="Johnson",
        date_of_birth=date(1995, 2, 10),
        phone_number="555-123-4567",
        address="789 Pine St",
        city="Denver",
        state="CO",
        country="USA"
    )
    
    profile_dict = profile.to_dict()
    
    assert profile_dict["profile_id"] == 5
    assert profile_dict["first_name"] == "Alice"
    assert profile_dict["last_name"] == "Johnson"
    assert profile_dict["date_of_birth"] == date(1995, 2, 10)
    assert profile_dict["phone_number"] == "555-123-4567"
    assert profile_dict["address"] == "789 Pine St"
    assert profile_dict["city"] == "Denver"
    assert profile_dict["state"] == "CO"
    assert profile_dict["country"] == "USA"
"""
def test_profile_missing_required_fields():
    with pytest.raises(TypeError):
        Profile()

def test_profile_invalid_types():
    with pytest.raises(TypeError):
        Profile(
            profile_id="10",
            user_id="user",
            first_name=123,
            last_name=456,
            date_of_birth="invalid_date",
            phone_number=789,
            address=101112,
            city=131415,
            state=161718,
            country=[]
        )
"""