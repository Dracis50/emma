"""auth_service/core/security.py – helpers mot-de-passe + JWT"""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

# --------------------------------------------------------------------------- #
# Password hashing : argon2 par défaut, encore capable de vérifier du bcrypt
# --------------------------------------------------------------------------- #
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],  # ordre = préférence
    default="argon2",
    deprecated="auto",
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


hash_password = get_password_hash  # alias rétro-compatibilité

# --------------------------------------------------------------------------- #
# JWT configuration
# --------------------------------------------------------------------------- #
def _get_secret() -> str:
    env_key = os.getenv("SECRET_KEY")
    if env_key:
        return env_key

    # Mode dev (pas de clé fournie) → on en forge une et on l’affiche
    import secrets, warnings

    random_key = secrets.token_urlsafe(64)
    warnings.warn(
        "SECRET_KEY manquant ! Clé aléatoire générée pour cette session :\n"
        f"   {random_key}\n"
        "⚠️  Ne faites *jamais* ça en production.",
        RuntimeWarning,
    )
    return random_key

SECRET_KEY: str = _get_secret()
ALGORITHM = "HS256"

# claims par défaut
ISSUER = "emma-auth-service"
AUDIENCE = "emma-users"

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 30


# --------------------------------------------------------------------------- #
# Token helpers
# --------------------------------------------------------------------------- #
def _build_claims(
    data: Dict[str, Any],
    expires_delta: timedelta,
    scope: str,
) -> Dict[str, Any]:
    """Assemble les claims communs pour access / refresh."""
    to_encode = data.copy()
    to_encode.update(
        {
            "exp": datetime.utcnow() + expires_delta,
            "iat": datetime.utcnow(),
            "iss": ISSUER,
            "aud": AUDIENCE,
            "scope": scope,
        }
    )
    return to_encode


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    claims = _build_claims(
        data=data,
        expires_delta=expires_delta
        or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        scope="access",
    )
    return jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    claims = _build_claims(
        data=data,
        expires_delta=expires_delta
        or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        scope="refresh",
    )
    return jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(
    token: str,
    expected_scope: str = "access",
) -> Optional[Dict[str, Any]]:
    """
    Décode un JWT et valide iss / aud / scope.
    Retourne le payload ou None si invalide / expiré.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            issuer=ISSUER,
            audience=AUDIENCE,
        )
        if payload.get("scope") != expected_scope:
            return None
        return payload
    except JWTError:
        return None
