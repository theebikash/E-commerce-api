# First Test: Home Endpoint
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "E-Commerce API is running"
    }


def test_protected_route_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_login_wrong_password(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "nonexistent_test_user",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401