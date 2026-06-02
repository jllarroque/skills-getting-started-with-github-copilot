"""
Backend API tests using AAA (Arrange-Act-Assert) pattern.
Tests cover all endpoints: GET /activities, POST /signup, DELETE /unregister, GET /
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: Fresh activities data is set up via fixture
        Act: GET /activities
        Assert: Status 200, all activities returned with correct structure
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(activities) == 3
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
    
    def test_get_activities_response_structure(self, client):
        """
        Arrange: Fresh activities data is set up via fixture
        Act: GET /activities
        Assert: Response has correct structure with all required fields
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        activity = activities["Chess Club"]
        
        # Assert
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)
        assert activity["max_participants"] == 12


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success_new_participant(self, client):
        """
        Arrange: New email not yet registered, existing activity
        Act: POST /signup with new email
        Assert: Status 200, participant added to activity
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        activities_after = client.get("/activities").json()
        
        # Assert
        assert response.status_code == 200
        assert new_email in activities_after[activity_name]["participants"]
        assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
    
    def test_signup_duplicate_email_returns_400(self, client):
        """
        Arrange: Email already registered for an activity
        Act: POST /signup with same email twice
        Assert: First succeeds (200), second fails (400)
        """
        # Arrange
        activity_name = "Chess Club"
        duplicate_email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": duplicate_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Arrange: Activity name that doesn't exist
        Act: POST /signup for non-existent activity
        Assert: Status 404
        """
        # Arrange
        nonexistent_activity = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_signup_updates_participant_count(self, client):
        """
        Arrange: Activity with known participant count
        Act: POST /signup with new email
        Assert: Participant count increases by 1
        """
        # Arrange
        activity_name = "Programming Class"
        initial_count = len(client.get("/activities").json()[activity_name]["participants"])
        new_email = "alice@mergington.edu"
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        updated_count = len(client.get("/activities").json()[activity_name]["participants"])
        
        # Assert
        assert updated_count == initial_count + 1


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success_removes_participant(self, client):
        """
        Arrange: Existing participant in activity
        Act: DELETE /unregister with their email
        Assert: Status 200, participant removed from activity
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )
        activities_after = client.get("/activities").json()
        
        # Assert
        assert response.status_code == 200
        assert email_to_remove not in activities_after[activity_name]["participants"]
        assert response.json()["message"] == f"Unregistered {email_to_remove} from {activity_name}"
    
    def test_unregister_nonregistered_email_returns_400(self, client):
        """
        Arrange: Email not registered for activity
        Act: DELETE /unregister with unregistered email
        Assert: Status 400
        """
        # Arrange
        activity_name = "Chess Club"
        unregistered_email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": unregistered_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client):
        """
        Arrange: Activity name that doesn't exist
        Act: DELETE /unregister from non-existent activity
        Assert: Status 404
        """
        # Arrange
        nonexistent_activity = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_updates_participant_count(self, client):
        """
        Arrange: Activity with known participant count
        Act: DELETE /unregister existing participant
        Assert: Participant count decreases by 1
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        initial_count = len(client.get("/activities").json()[activity_name]["participants"])
        
        # Act
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )
        updated_count = len(client.get("/activities").json()[activity_name]["participants"])
        
        # Assert
        assert updated_count == initial_count - 1


class TestRootRedirect:
    """Tests for GET / endpoint"""
    
    def test_root_redirects_to_index(self, client):
        """
        Arrange: TestClient ready
        Act: GET /
        Assert: Returns redirect to /static/index.html
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
