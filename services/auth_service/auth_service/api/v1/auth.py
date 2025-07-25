# auth_service/api/v1/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth_service.schemas.user import LoginRequest, Token
from auth_service.models.user import User
from auth_service.database import get_db
from auth_service.core.security import verify_password
from auth_service.core.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(
        request.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=401, detail="Incorrect email or password"
        )
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
