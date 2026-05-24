import pytest
from app.auth.password_service import PasswordService


@pytest.fixture
def pwd():
    return PasswordService()


def test_hash_is_not_plaintext(pwd):
    hashed = pwd.hash("secret123")
    assert hashed != "secret123"


def test_verify_correct_password(pwd):
    hashed = pwd.hash("mypassword")
    assert pwd.verify("mypassword", hashed) is True


def test_verify_wrong_password(pwd):
    hashed = pwd.hash("mypassword")
    assert pwd.verify("wrongpassword", hashed) is False


def test_hash_is_different_each_time(pwd):
    h1 = pwd.hash("same")
    h2 = pwd.hash("same")
    assert h1 != h2