def test_user_register(test_client):
    """
    GIVEN a Flask application
    WHEN the '/register' page (POST)ed right
    THEN check that a '200' status code is returned
    THEN check that the email returned is the same
    """
    response = test_client.post("/register", json={
        'password': 'gancho',
        'email': 'dannyf@d300.org'
        })

    assert response.status_code == 200
    assert response.json["email"] == 'dannyf@d300.org'


def test_user_login(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page (POST)ed right
    THEN check that a '201' status code is returned
    THEN check that a string-like token thing is returned
    """
    response = test_client.post("/login", json={
        'password': 'gancho',
        'email': 'dannyf@d300.org'
        })
    assert response.status_code == 201
    assert isinstance(response.json["token"], str)

# user edit

# user delete