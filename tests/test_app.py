from urllib.parse import quote


def test_get_activities_returns_all_activities(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert isinstance(activities["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    response = client.get("/activities")
    assert email in response.json()[activity_name]["participants"]


def test_signup_for_activity_rejects_duplicate_signup(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{quote(activity_name)}/participants?email={quote(email)}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    response = client.get("/activities")
    assert email not in response.json()[activity_name]["participants"]


def test_unregister_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "ghost@mergington.edu"

    # Act
    response = client.delete(f"/activities/{quote(activity_name)}/participants?email={quote(email)}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
