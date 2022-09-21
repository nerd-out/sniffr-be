def test_home_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Sniffr's" in response.data

def test_user_login(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page (POST)ed right
    THEN check that a '200' status code is returned
    """
    response = test_client.post("/register", json={
        'password': 'gancho',
        'email': 'dannyf@d300.org'
        })

    assert response.status_code == 200
    assert response.json["email"] == 'dannyf@d300.org'


def test_user_create(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page (POST)ed right
    THEN check that a '200' status code is returned
    """
    response = test_client.post("/login", json={
        'password': 'gancho',
        'email': 'dannyf@d300.org'
        })
    assert response.status_code == 201
    assert isinstance(response.json["token"], str)