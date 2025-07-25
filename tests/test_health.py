from fastapi.testclient import TestClient
from auth_service.main import app

client = TestClient(app)


def test_health_endpoint():
    """Le /healthz doit répondre 200 et {'status': 'ok'}."""
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
