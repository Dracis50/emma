# auth_service/main.py
from dotenv import load_dotenv
from fastapi import FastAPI

from auth_service.api.v1 import users, auth

load_dotenv()

app = FastAPI(title="EMMA Auth Service", version="0.1.0")

app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")

# ➜  AJOUTE CE BLOC ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
@app.get("/healthz", include_in_schema=False)
def healthcheck():
    """
    Traefik et les sondes Kubernetes appellent /healthz pour savoir
    si l’API est vivante ; on renvoie simplement 200 + un petit JSON.
    """
    return {"status": "ok"}
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
