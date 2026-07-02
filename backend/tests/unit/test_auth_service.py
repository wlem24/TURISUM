import pytest
from app.core.security.password import hash_password, verify_password
from app.core.security.jwt import create_access_token, verify_access_token, create_refresh_token, verify_refresh_token
import uuid


def test_password_hash_verify():
    plain = "MySecret123!"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed) is True


def test_wrong_password_fails():
    hashed = hash_password("correct")
    assert verify_password("wrong", hashed) is False


def test_access_token_encode_decode():
    user_id = uuid.uuid4()
    token = create_access_token(user_id, "visitor")
    payload = verify_access_token(token)
    assert payload is not None
    assert payload["sub"] == str(user_id)
    assert payload["role"] == "visitor"
    assert payload["type"] == "access"


def test_refresh_token_encode_decode():
    user_id = uuid.uuid4()
    token = create_refresh_token(user_id)
    payload = verify_refresh_token(token)
    assert payload is not None
    assert payload["sub"] == str(user_id)
    assert payload["type"] == "refresh"


def test_access_token_rejected_as_refresh():
    user_id = uuid.uuid4()
    token = create_access_token(user_id, "admin")
    assert verify_refresh_token(token) is None


def test_invalid_token_returns_none():
    assert verify_access_token("not.a.real.token") is None
