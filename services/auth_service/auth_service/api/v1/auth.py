# auth_service/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth_service.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_access_token,
)
from auth_service.database import get_db
from auth_service.models.user import User
from auth_service.schemas.user import (
    LoginRequest,
    TokenPair,
    AccessToken,
)

router = APIRouter(prefix="/auth", tags=["auth"])

# ------------- stockage naïf des RT rotés -------------
REFRESH_TOKEN_BLACKLIST: set[str] = set()


# ──────────────────────────
# POST /login
# ──────────────────────────
@router.post("/login", response_model=TokenPair, status_code=status.HTTP_200_OK)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user: User | None = (
        db.query(User).filter(User.email == req.email).first()
    )
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    payload = {"sub": str(user.id), "email": user.email}

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# ──────────────────────────
# POST /refresh
# ──────────────────────────
class RefreshRequest(LoginRequest.model_construct(__pydantic_fields_set__={})) :  # reuse BaseModel machinery
    refresh_token: str


@router.post(
    "/refresh",
    response_model=AccessToken,
    status_code=status.HTTP_200_OK,
)
def refresh(req: RefreshRequest):
    old_rt = req.refresh_token

    # vérifie signature + scope
    payload = decode_access_token(old_rt, expected_scope="refresh")
    if payload is None or old_rt in REFRESH_TOKEN_BLACKLIST:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    # rotation : invalide l’ancien RT
    REFRESH_TOKEN_BLACKLIST.add(old_rt)

    new_payload = {
        "sub": payload["sub"],
        "email": payload["email"],
    }
    access_token = create_access_token(new_payload)
    refresh_token = create_refresh_token(new_payload)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
