import pytest


def test_register_new_user(client):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_register_duplicate_user(client):
    client.post("/auth/register", json={"username": "dup", "password": "pass"})
    response = client.post("/auth/register", json={"username": "dup", "password": "pass"})
    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={"username": "loginuser", "password": "pass123"})
    response = client.post("/auth/login", json={"username": "loginuser", "password": "pass123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "user2", "password": "correct"})
    response = client.post("/auth/login", json={"username": "user2", "password": "wrong"})
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/auth/login", json={"username": "nobody", "password": "pass"})
    assert response.status_code == 401