from fastapi.testclient import TestClient
from auth_service.main import app
from auth_service.core.security import get_password_hash
from auth_service.database import SessionLocal, init_db
from auth_service.models.user import User

client = TestClient(app)


def _ensure_demo_user():
    init_db()
    db = SessionLocal()
    if not db.query(User).filter_by(email="demo@example.com").first():
        db.add(
            User(
                email="demo@example.com",
                hashed_password=get_password_hash("changeme"),
                is_active=True,
            )
        )
        db.commit()
    db.close()


def test_login_and_protected_route():
    _ensure_demo_user()

    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "demo@example.com", "password": "changeme"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]

    resp2 = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp2.status_code == 200
    assert resp2.json()["email"] == "demo@example.com"
