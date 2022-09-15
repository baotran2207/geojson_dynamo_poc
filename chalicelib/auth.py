import hashlib
from uuid import uuid4

import jwt
from chalice import AuthResponse, UnauthorizedError

from chalicelib.config import settings


def get_jwt_token(username, password, hashed_pass, secret=settings.secret_key):
    if verify_password(password, hashed_pass):
        payload = {
            "username": username,
            "jti": str(uuid4()),
        }
        return jwt.encode(payload, secret, algorithm="HS256")
    raise UnauthorizedError("Invalid password")


def decode_jwt_token(token: str, secret: str = settings.secret_key):
    return jwt.decode(token, secret, algorithms=["HS256"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password


def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
