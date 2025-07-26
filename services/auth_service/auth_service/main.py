# auth_service/main.py
from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from dotenv import load_dotenv
import logging

from auth_service.api.v1 import users, auth
from auth_service.database import init_db
from contextlib import asynccontextmanager

load_dotenv()


# ------------------------------------------------------------------ #
# Logging minimal : niveau INFO, horodatage court
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("emma.auth")
# ------------------------------------------------------------------ #


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("⏳  Initialisation des tables…")
    init_db()
    logger.info("✅  Base prête.")
    yield
    # Ici tu pourrais fermer proprement des connexions, etc.


# instancie SlowAPI limiter (IP-based)
limiter = Limiter(key_func=get_remote_address)


app = FastAPI(
    title="EMMA Auth Service",
    version="1.1.0",
    lifespan=lifespan,
)

# active le rate‐limit middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# routes métiers
app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router,  prefix="/api/v1")


@app.get("/healthz", include_in_schema=False)
def healthcheck():

    return {"status": "ok"}
