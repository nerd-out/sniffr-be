from sniffr.models import User, db

def test_get_all_dogs(test_client):
    """
    GIVEN a Flask application
    WHEN the '/dogs' page is sent a GET
    THEN check that a '200' status code is returned
    THEN check that the email returned is the same
    """
    # Register user using post request
    response = test_client.get("/dogs")
    content = response.json


    # Assert
    assert response.status_code == 200
    assert len(content) == 6 # number of dogs in database at time of writing

def test_get_one_dog(test_client):
    """
    GIVEN a Flask application
    WHEN the '/dog/dogid' page is sent a GET
    THEN check that a '200' status code is returned
    THEN check that the email returned is the same
    """
    # Register user using post request
    response = test_client.get("/dog/1")
    content = response.json


    # Assert
    assert response.status_code == 200
    assert content['dog_name'] == 'Augie'


def test_new_dog_register(test_existing_user_fixture, test_client):
    """
    GIVEN a Flask application
    WHEN the '/dog' page is sent a POST
    THEN check that a '200' status code is returned
    THEN check that the info returned is the same
    """
    # Format json post
    login_token = test_existing_user_fixture['token']
    # Assemble Headers
    headers = {"x-access-token": login_token}

    # Register dog using post request
    create_json = {
        "dog_name": "Ein",
        "breed_id": 110,
        "size_id": 1,
        "temperament_id": 2,
        "age": '24',
        "sex": "Data Dog",
        "is_vaccinated": False,
        "is_fixed": False,
        "dog_bio": """Ein (アイン Ain?) is a Pembroke Welsh Corgi and "data dog," meaning that his intelligence was greatly enhanced by a research facility. What exactly was done to him was not widely known. Ein became part of the Bebop crew and was a good friend of Edward.""",
        "dog_pic": "Ein driving a car pic",
        "activities": [3]}

    response = test_client.post("/dog", json=create_json, headers=headers)
    content = response.json

    # Check status code & that contents updated
    assert response.status_code == 200
    assert content["dog_name"] == create_json["dog_name"]
    assert content["breed_id"] == create_json["breed_id"]
    assert content["size_id"] == create_json["size_id"]
    assert content["temperament_id"] == create_json["temperament_id"]
    assert content["owner_id"] == 1
    assert content["age"] == create_json["age"]
    assert content["sex"] == create_json["sex"]
    assert content["is_vaccinated"] == create_json["is_vaccinated"]
    assert content["is_fixed"] == create_json["is_fixed"]
    assert content["dog_bio"] == create_json["dog_bio"]
    assert content["dog_pic"] == create_json["dog_pic"]

def test_edit_new_dog(test_existing_user_fixture, test_client):
    """
    GIVEN a Flask application
    WHEN the '/dog' page is sent a POST
    THEN check that a '200' status code is returned
    THEN check that the info returned is the same
    """
    # Format json post
    login_token = test_existing_user_fixture['token']
    # Assemble Headers
    headers = {"x-access-token": login_token}

    # Register dog using post request
    create_json = {
        "dog_name": "Ein",
        "breed_id": 110,
        "size_id": 1,
        "temperament_id": 2,
        "age": '24',
        "sex": "Data Dog",
        "is_vaccinated": False,
        "is_fixed": False,
        "dog_bio": """Ein is a Pembroke Welsh Corgi and "data dog," meaning his intelligence was greatly enhanced by a research facility.""",
        "dog_pic": "Ein driving a car pic",
        "activities": [1, 2]}

    response = test_client.post("/dog", json=create_json, headers=headers)
    content = response.json

    # Check status code & that contents updated
    assert response.status_code == 200
    assert content["dog_name"] == create_json["dog_name"]
    assert content["breed_id"] == create_json["breed_id"]
    assert content["size_id"] == create_json["size_id"]
    assert content["temperament_id"] == create_json["temperament_id"]
    assert content["owner_id"] == 1
    assert content["age"] == create_json["age"]
    assert content["sex"] == create_json["sex"]
    assert content["is_vaccinated"] == create_json["is_vaccinated"]
    assert content["is_fixed"] == create_json["is_fixed"]
    assert content["dog_bio"] == create_json["dog_bio"]
    assert content["dog_pic"] == create_json["dog_pic"]

def test_delete_new_dog(test_existing_user_fixture, test_client):
    """
    GIVEN a Flask application
    WHEN the '/dog' page is sent a POST
    THEN check that a '200' status code is returned
    THEN check that the info returned is the same
    """
    # Format json post
    login_token = test_existing_user_fixture['token']
    # Assemble Headers
    headers = {"x-access-token": login_token}

    # Register dog using post request
    create_json = {
        "dog_name": "Ein",
        "breed_id": 110,
        "size_id": 1,
        "temperament_id": 2,
        "age": '24',
        "sex": "Data Dog",
        "is_vaccinated": False,
        "is_fixed": False,
        "dog_bio": """Ein is a Pembroke Welsh Corgi and "data dog," meaning his intelligence was greatly enhanced by a research facility.""",
        "dog_pic": "Ein driving a car pic",
        "activities": [3, 4]}
    response = test_client.post("/dog", json=create_json, headers=headers)
    content = response.json

    # Delete the dog
    response = test_client.delete(f"/dog/{str(content['dog_id'])}", headers=headers)
    content = response.json

    assert response.status_code == 200
