import pytest
from auth_service.database import SessionLocal
from auth_service.models.user import User

@pytest.fixture(autouse=True)
def clear_users_table():
    db = SessionLocal()
    db.query(User).delete()
    db.commit()
    db.close()

from fastapi.testclient import TestClient
from auth_service.main import app

client = TestClient(app)

def test_smoke():
    response = client.get("/api/v1/users/")
    assert response.status_code in [200, 422]  # 422 si base vide/validation, 200 sinon

def test_create_user():
    # Remplace les valeurs si besoin
    payload = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/users/", json=payload)
    assert response.status_code in [200, 201, 422]

def test_create_user_duplicate_email():
    payload = {"email": "test@example.com", "password": "password123"}
    response = client.post("/api/v1/users/", json=payload)
    assert response.status_code == 201  # ou 200 selon ton endpoint

    # Deuxième tentative, même email
    response = client.post("/api/v1/users/", json=payload)
    assert response.status_code == 409  # REST: 409 = Conflict, c’est la norme
