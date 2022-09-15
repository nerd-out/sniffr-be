from sniffr.app import create_app

def test_login_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page (POST)ed right
    THEN check that a '200' status code is returned
    """
    response = test_client.post("/login", json={
        'password': 'windows',
        'email': 'jon@sniffr.be'
        })

    assert response.status_code == 201
    assert isinstance(response.json["token"], str)

