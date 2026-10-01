def test_get_products(client):
    response = client.get("/products/")

    assert response.status_code == 200

    assert isinstance(response.json(), list)