"""
Pytest configuration and fixtures for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app
import copy


# Sample activities data for testing
SAMPLE_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
}


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient with fresh, isolated activities data.
    Resets activities before each test to prevent data pollution.
    """
    # Import the activities dict from the app
    from src import app as app_module
    
    # Store original activities
    original_activities = copy.deepcopy(app_module.activities)
    
    # Reset activities to sample data for testing
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(SAMPLE_ACTIVITIES))
    
    # Create test client
    test_client = TestClient(app)
    
    yield test_client
    
    # Restore original activities after test
    app_module.activities.clear()
    app_module.activities.update(original_activities)
