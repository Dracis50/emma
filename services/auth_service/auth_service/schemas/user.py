# auth_service/schemas/user.py

from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    # Au login on ne filtre pas sur la longueur : une chaîne vide déclenchera
    # déjà un 422 « value_error.missing ».  
    # Laisse la logique d’auth renvoyer 401 si le mot de passe est faux.
    password: str
    is_active: bool = True
    is_admin: bool = False
    is_premium: bool = False


class UserRead(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    is_premium: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
