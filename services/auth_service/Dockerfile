# --- build image -------------------------------------------------------------
FROM python:3.9-slim

WORKDIR /app

# 1/ Dépendances Python (sans installer le projet)
COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

# --- petit outil debug optionnel
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# 2/ Code du service
COPY . .

# 3/ On installe maintenant le projet (il existe enfin)
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD ["uvicorn", "auth_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
