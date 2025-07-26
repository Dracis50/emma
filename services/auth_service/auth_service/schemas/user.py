# auth_service/schemas/user.py
from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: constr(min_length=8)
    is_active: bool = True
    is_admin: bool = False
    is_premium: bool = False


class UserRead(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    is_premium: bool

    model_config = dict(from_attributes=True)  # Pydantic v2 – ORM mode


# ──────────────────────
# Tokens & payloads
# ──────────────────────
class TokenPair(BaseModel):
    """Réponse standard : access + refresh."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AccessToken(BaseModel):
    """Réponse d’un /refresh : nouveau token d’accès (et rotation RT)."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str  # pas de min_length ici → renvoie 401 si mauvais
