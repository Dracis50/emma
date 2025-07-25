import os

# auth_service/core/security.py

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:

    return pwd_context.hash(password)


hash_password = get_password_hash


# JWT config (optionnel si déjà dans core.security.py)
SECRET_KEY = os.getenv("SECRET_KEY") or "insecure-dev-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,   # ✅ compatible Py-3.9
) -> str:
    """
    Génère un JWT signé contenant `data` + date d’expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    """
    Décode le JWT ; renvoie le payload dict ou None si signature / date invalides.
    """
    from jose import JWTError

    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
