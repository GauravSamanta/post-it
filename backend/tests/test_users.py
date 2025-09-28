import pytest
from fastapi.testclient import TestClient


def test_create_user(client: TestClient, test_user):
    response = client.post("/api/v1/users/", json=test_user)
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]
    assert "id" in data
    assert "hashed_password" not in data


def test_create_user_duplicate_email(client: TestClient, test_user):
    # Create user first time
    response = client.post("/api/v1/users/", json=test_user)
    assert response.status_code == 200

    # Try to create user with same email
    response = client.post("/api/v1/users/", json=test_user)
    assert response.status_code == 400


def test_get_users_unauthorized(client: TestClient):
    response = client.get("/api/v1/users/")
    assert response.status_code == 401


def test_get_user_by_id(client: TestClient, test_user):
    # Create user and login
    create_response = client.post("/api/v1/users/", json=test_user)
    user_id = create_response.json()["id"]

    login_data = {
        "username": test_user["email"],
        "password": test_user["password"],
    }
    login_response = client.post("/api/v1/auth/login", data=login_data)
    token = login_response.json()["access_token"]

    # Get user by ID
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/api/v1/users/{user_id}", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == test_user["email"]
