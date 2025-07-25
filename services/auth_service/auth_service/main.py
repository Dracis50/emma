# auth_service/main.py
from fastapi import FastAPI
from dotenv import load_dotenv

from auth_service.api.v1 import users, auth
from auth_service.database import init_db

load_dotenv()
app = FastAPI(title="EMMA Auth Service", version="0.1.0")

# routes métiers
app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router,  prefix="/api/v1")


@app.get("/healthz", include_in_schema=False)
def healthcheck():

    return {"status": "ok"}

@app.on_event("startup")
def _startup() -> None:
    """
    Au démarrage de l’API on crée les tables si elles n’existent pas.
    """
    init_db()
