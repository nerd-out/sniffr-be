def test_get_all_sizes(test_client):
    response = test_client.get("/sizes")
    content = response.json

    # Assert
    assert response.status_code == 200
    assert len(content) == 6