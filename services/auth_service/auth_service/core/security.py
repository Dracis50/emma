"""Security utilities for password hashing and opaque token generation.
This module replaces external dependencies like passlib and python-jose with
simple in-memory implementations suitable for testing and development.
"""

import os
import secrets
import hashlib
import datetime as dt
from typing import Dict, Any, Optional
from fastapi import HTTPException, status

# Secret key for salting password hashes and signing tokens
SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
# Default expiration durations (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour
REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

# In-memory token store. Each token maps to its payload, expiry and scope.
_TOKEN_STORE: Dict[str, Dict[str, Any]] = {}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return get_password_hash(plain_password) == hashed_password


def get_password_hash(password: str) -> str:
    """Hash a password using SHA-256 with a secret key salt."""
    return hashlib.sha256((password + SECRET_KEY).encode()).hexdigest()


def _create_token(data: Dict[str, Any], expires_delta: dt.timedelta, scope: str) -> str:
    """Create a new opaque token and store it in the in-memory token store."""
    token = secrets.token_urlsafe(32)
    expire = dt.datetime.utcnow() + expires_delta
    # Store payload and metadata
    _TOKEN_STORE[token] = {"payload": data, "expire": expire, "scope": scope}
    return token


def create_access_token(data: Dict[str, Any], expires_delta: Optional[dt.timedelta] = None) -> str:
    """Generate a new access token for the given payload."""
    if expires_delta is None:
        expires_delta = dt.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(data, expires_delta, scope="access")


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[dt.timedelta] = None) -> str:
    """Generate a new refresh token for the given payload."""
    if expires_delta is None:
        expires_delta = dt.timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return _create_token(data, expires_delta, scope="refresh")


def decode_access_token(token: str, scope: str = "access") -> Dict[str, Any]:
    """Decode an opaque token and return its payload if valid.

    Raises HTTPException if the token is invalid, expired, or the scope
    does not match.
    """
    token_data = _TOKEN_STORE.get(token)
    if not token_data or token_data.get("scope") != scope:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    if dt.datetime.utcnow() > token_data.get("expire"):
        # Remove expired token
        _TOKEN_STORE.pop(token, None)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

    return token_data.get("payload", {})
