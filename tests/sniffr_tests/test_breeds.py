
def test_get_all_breeds(test_client):
    response = test_client.get("/breeds")
    content = response.json

    # Assert
    assert response.status_code == 200
    assert len(content) == 153