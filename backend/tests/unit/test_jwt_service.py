import pytest
import time
from app.auth.jwt_service import JWTService


@pytest.fixture
def jwt():
    return JWTService()


def test_create_token_returns_string(jwt):
    token = jwt.create_token(user_id=1)
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_valid_token(jwt):
    token = jwt.create_token(user_id=42)
    payload = jwt.verify_token(token)
    assert payload is not None
    assert payload["sub"] == "42"


def test_verify_invalid_token_returns_none(jwt):
    result = jwt.verify_token("this.is.invalid")
    assert result is None


def test_verify_tampered_token_returns_none(jwt):
    token = jwt.create_token(user_id=1)
    tampered = token[:-5] + "XXXXX"
    result = jwt.verify_token(tampered)
    assert result is None


def test_token_contains_exp(jwt):
    token = jwt.create_token(user_id=1)
    payload = jwt.verify_token(token)
    assert "exp" in payload