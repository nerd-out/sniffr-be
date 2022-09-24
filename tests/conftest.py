from sniffr.app import create_app
import pytest
from seed_db import seed_db


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            seed_db()
            yield testing_client


@pytest.fixture(scope="module")
def new_user_fixture(test_client):
    response = test_client.post(
        "/login", json={"password": "gancho", "email": "dannyf@d300.org"}
    )

    return response


@pytest.fixture(scope="module")
def existing_user_fixture(test_client):
    response = test_client.post(
        "/login", json={"password": "windows", "email": "jon@sniffr.be"}
    )

    return response


@pytest.fixture(scope="module")
def new_dog_fixture(test_client):
    response = test_client.post(
        "/dog",
        json={
            "dog_name": "Ein",
            "breed_id": 110,
            "size_id": 1,
            "temperament_id": 2,
            "owner_id": 1,
            "age": 24,
            "sex": "Data Dog",
            "is_vaccinated": False,
            "is_fixed": False,
            "dog_bio": """Ein (アイン Ain?) is a Pembroke Welsh Corgi and "data dog," meaning that his intelligence was greatly enhanced by a research facility. What exactly was done to him was not widely known. Ein became part of the Bebop crew and was a good friend of Edward.""",
            "dog_pic": "Ein driving a car pic",
        },
    )

    return response


@pytest.fixture(scope='module')
def test_existing_user_fixture(test_client):
    response = test_client.post("/login", json={"password": "windows", "email": "jon@sniffr.be"})
    
    login_content = response.json

    return login_content
