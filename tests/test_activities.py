def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activities = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Yoga Club",
        "Art Studio",
        "Drama Workshop",
        "Science Club",
        "Math Circle",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == expected_activities


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Soccer Team"
    email = "alex@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activity_response = client.get("/activities")
    assert email in activity_response.json()[activity_name]["participants"]


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    activity_response = client.get("/activities")
    assert email not in activity_response.json()[activity_name]["participants"]


def test_remove_nonexistent_participant_returns_400(client):
    # Arrange
    activity_name = "Programming Class"
    email = "notfound@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Participant not found for this activity"


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "jane@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
