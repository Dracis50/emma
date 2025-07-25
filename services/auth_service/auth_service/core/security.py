"""auth_service/core/security.py – helpers mot-de-passe + JWT"""

import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Any

from jose import JWTError, jwt
from passlib.context import CryptContext

# --------------------------------------------------------------------------- #
# Password hashing
# --------------------------------------------------------------------------- #
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


hash_password = get_password_hash  # alias rétro-compatibilité

# --------------------------------------------------------------------------- #
# JWT helpers
# --------------------------------------------------------------------------- #
SECRET_KEY = os.getenv("SECRET_KEY", "insecure-dev-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Génère un JWT signé contenant `data` et une date d’expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Décodage sécurisé ; retourne None si signature ou exp invalide."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
