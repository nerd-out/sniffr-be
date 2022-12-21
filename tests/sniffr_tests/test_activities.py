
def test_get_all_activities(test_client):
    response = test_client.get("/activities")
    content = response.json

    # Assert
    assert response.status_code == 200
    assert len(content) == 9


def test_get_specific_activity(test_client):
    response = test_client.get("/activity/1")
    content = response.json

    # Assert
    assert response.status_code == 200
    assert content[0]["activity_description"] == "Walks"


def test_create_activity(test_client):
    # Get number of activities
    all_activities = test_client.get("/activities")
    content = all_activities.json
    number_of_activities = len(content)

    # Make post request
    response = test_client.post(
        "/activity", json={"activity_description": "Cry"}
    )

    # Get number of activities
    after_all_activities = test_client.get("/activities")
    after_content = after_all_activities.json
    after_number_of_activities = len(after_content)

    # Assert
    assert response.status_code == 200
    assert response.json["activity_description"] == "Cry"
    assert after_number_of_activities == number_of_activities + 1