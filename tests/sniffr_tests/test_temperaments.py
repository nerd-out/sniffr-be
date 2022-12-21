def test_get_all_temperaments(test_client):
    response = test_client.get("/temperaments")
    content = response.json

    # Assert
    assert response.status_code == 200
    assert len(content) == 6