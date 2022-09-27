def test_new_user_register(test_client):
    """
    GIVEN a Flask application
    WHEN the '/register' page (POST)ed right
    THEN check that a '200' status code is returned
    THEN check that the email returned is the same
    """
    # Register user using post request
    response = test_client.post(
        "/register", json={"password": "gancho", "email": "dannyf@d300.org"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json["email"] == "dannyf@d300.org"


def test_new_user_login(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page (POST)ed right
    THEN check that a '201' status code is returned
    THEN check that a string-like token thing is returned
    """
    # Login as user using post request
    response = test_client.post(
        "/login", json={"password": "gancho", "email": "dannyf@d300.org"}
    )

    assert response.status_code == 201
    assert isinstance(response.json["token"], str)


def test_edit_new_user(new_user_fixture, test_client):
    """
    GIVEN a Flask application
    WHEN the '/edit' page (POST)ed right
    THEN check that a '410' status code is returned
    THEN check that the correct message is returned
    """
    # Format json post
    content = new_user_fixture.json

    # Assemble login headers
    headers = {"x-access-token": content["token"]}

    # Create edit json
    edit_json = {
        "email": "danimal@d300.org",
        "birthday": "30",
        "gender": "Dude",
        "max_distance": 10,
        "name": "Dan Finger",
        "user_bio": "Worthless",
        "zipcode": "00000",
        "user_pic": "^_^",
    }

    # Delete user
    response = test_client.post("/user/edit", headers=headers, json=edit_json)
    content = response.json

    # Check status code & that contents updated
    assert response.status_code == 200
    assert content["email"] == edit_json["email"]
    assert content["birthday"] == edit_json["birthday"]
    assert content["gender"] == edit_json["gender"]
    assert content["max_distance"] == edit_json["max_distance"]
    assert content["name"] == edit_json["name"]
    assert content["user_bio"] == edit_json["user_bio"]
    assert content["user_pic"] == edit_json["user_pic"]


def test_delete_new_user(new_user_fixture, test_client):
    """
    GIVEN a Flask application
    WHEN the '/delete' page is sent a (DELETE)ed
    THEN check that a '410' status code is returned
    THEN check that the correct message is returned
    """
    # Format json post
    content = new_user_fixture.json

    # Assemble Headers
    headers = {"x-access-token": content["token"]}

    # Delete user
    response = test_client.delete("/user", headers=headers)

    # Assert
    assert response.status_code == 200
