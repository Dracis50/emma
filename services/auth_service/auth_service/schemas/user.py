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

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
