from sniffr.app import create_app
import pytest
from seed_db import seed_db

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            seed_db()
            yield testing_client

@pytest.fixture(scope='module')
def new_user_fixture(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page (POST)ed right
    THEN check that a '201' status code is returned
    THEN check that a string-like token thing is returned
    """
    response = test_client.post("/login", json={ 
        'password': 'gancho',
        'email': 'dannyf@d300.org'})

    return response