# auth_service/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import urllib.parse as ul
from sqlalchemy.exc import OperationalError
import time

# 1️⃣  Priorité à DATABASE_URL si elle existe
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    # Sinon on reconstruit l’URL à partir des composantes
    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASS = ul.quote_plus(os.getenv("POSTGRES_PASSWORD", "postgres"))
    DB_HOST = os.getenv("POSTGRES_HOST", "db")          # ← par défaut “db”
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")
    DB_NAME = os.getenv("POSTGRES_DB", "emma")
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def init_db(retries: int = 10, delay: float = 2.0) -> None:

    """
    Crée les tables. Ré-essaie tant que PostgreSQL n’est pas prêt.
    """

    for attempt in range(1, retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            print("✅  Tables créées.")
            return
        except OperationalError as exc:
            print(f"⏳  DB pas prête ({exc}); retry {attempt}/{retries}…")
            time.sleep(delay)

    # Si on arrive ici, c’est que Postgres n’a jamais répondu
    raise RuntimeError("❌  Impossible de se connecter à PostgreSQL.")

# Dépendance FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
