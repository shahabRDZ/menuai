from uuid import uuid4

from app.services.security import PasswordHasher, TokenService


def test_password_hasher_roundtrip():
    hasher = PasswordHasher()
    h = hasher.hash("correct horse battery staple")
    assert hasher.verify("correct horse battery staple", h)
    assert not hasher.verify("wrong password", h)


def test_token_service_roundtrip():
    tokens = TokenService(secret="test-secret", algorithm="HS256", expire_minutes=5)
    uid = uuid4()
    assert tokens.verify(tokens.issue(uid)) == uid


def test_invalid_token_is_rejected():
    tokens = TokenService(secret="test-secret", algorithm="HS256", expire_minutes=5)
    assert tokens.verify("not-a-real-token") is None
