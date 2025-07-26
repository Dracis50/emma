# auth_service/core/deps.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from auth_service.database import get_db
from auth_service.models.user import User
from auth_service.core.security import decode_access_token

# Le bon endpoint (vérifie bien le chemin)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    # 1) on valide signature + scope=access
    payload = decode_access_token(token, expected_scope="access")
    if payload is None:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials"
        )

    # 2) on cherche d’abord par id (sub), sinon par email
    user = None

    # sub doit idéalement contenir l’ID numérique
    sub = payload.get("sub")
    if sub is not None:
        try:
            user = db.query(User).filter(User.id == int(sub)).first()
        except (ValueError, TypeError):
            # sub n’était pas un entier → on tentera l’email
            pass

    if user is None and "email" in payload:
        user = (
            db.query(User)
            .filter(User.email == payload["email"])
            .first()
        )

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
