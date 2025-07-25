# auth_service/core/security.py

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:        # 👈 nouveau
    return pwd_context.hash(password)

hash_password = get_password_hash                   # 👈 alias (facultatif)


# JWT config (optionnel si déjà dans core.security.py)
import os
SECRET_KEY = os.getenv("SECRET_KEY") or "insecure-dev-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Génére un JWT signé contenant le payload `data` + date d’expiration.
    - `data` doit déjà contenir la clé « sub » (subject = email).
    - `expires_delta` surcharge la durée par défaut (60 min).
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """Retourne le payload décodé ou `None` si signature / exp invalide."""
    from jose import JWTError

    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
