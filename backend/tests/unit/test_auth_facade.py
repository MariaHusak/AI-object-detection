import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.facades.auth_facade import AuthFacade


@pytest.fixture
def facade():
    users = MagicMock()
    password = MagicMock()
    jwt = MagicMock()
    return AuthFacade(users, password, jwt), users, password, jwt


def test_register_success(facade):
    auth, users, password, jwt = facade
    users.get_by_username.return_value = None
    users.create.return_value = MagicMock(id=1, username="alice")
    password.hash.return_value = "hashed"

    result = auth.register("alice", "pass123")
    assert result["username"] == "alice"
    assert result["id"] == 1


def test_register_existing_user_raises(facade):
    auth, users, password, jwt = facade
    users.get_by_username.return_value = MagicMock()  # вже існує

    with pytest.raises(HTTPException) as exc:
        auth.register("alice", "pass")
    assert exc.value.status_code == 400


def test_login_success(facade):
    auth, users, password, jwt = facade
    users.get_by_username.return_value = MagicMock(id=1, password="hashed")
    password.verify.return_value = True
    jwt.create_token.return_value = "token123"

    result = auth.login("alice", "pass")
    assert result["access_token"] == "token123"


def test_login_wrong_password_raises(facade):
    auth, users, password, jwt = facade
    users.get_by_username.return_value = MagicMock(id=1, password="hashed")
    password.verify.return_value = False

    with pytest.raises(HTTPException) as exc:
        auth.login("alice", "wrong")
    assert exc.value.status_code == 401


def test_login_user_not_found_raises(facade):
    auth, users, password, jwt = facade
    users.get_by_username.return_value = None

    with pytest.raises(HTTPException) as exc:
        auth.login("ghost", "pass")
    assert exc.value.status_code == 401