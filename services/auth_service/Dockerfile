FROM python:3.9-slim

WORKDIR /app

# ─── 1) Dépendances Python ─────────────────────────────────────────────
COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

# ─── 2) Code de l’application ──────────────────────────────────────────
COPY . .

# On installe maintenant **le projet** lui-même
RUN poetry install --only-root --no-interaction --no-ansi

EXPOSE 8000
CMD ["uvicorn", "auth_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
