import pytest


def _register_and_login(client, username="statuser", password="pass"):
    client.post("/auth/register", json={"username": username, "password": password})
    resp = client.post("/auth/login", json={"username": username, "password": password})
    return resp.json()["access_token"]


def test_stats_requires_auth(client):
    response = client.get("/stats/")
    assert response.status_code in (401, 403)


def test_stats_empty_for_new_user(client):
    token = _register_and_login(client)
    response = client.get("/stats/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["processed"] == 0