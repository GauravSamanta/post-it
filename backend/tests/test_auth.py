import pytest
from fastapi.testclient import TestClient


def test_login_success(client: TestClient, test_user):
    # First create a user
    response = client.post("/api/v1/users/", json=test_user)
    assert response.status_code == 200

    # Then try to login
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"],
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    login_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword",
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401


def test_get_current_user(client: TestClient, test_user):
    # Create user and login
    client.post("/api/v1/users/", json=test_user)
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"],
    }
    login_response = client.post("/api/v1/auth/login", data=login_data)
    token = login_response.json()["access_token"]

    # Get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]


def test_get_current_user_invalid_token(client: TestClient):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 403

