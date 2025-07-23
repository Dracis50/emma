# Utilise l’image officielle Python
FROM python:3.9-slim

# Installer Poetry
RUN pip install --no-cache-dir poetry

# Créer le dossier de l’app
WORKDIR /app

# Copier les fichiers de dépendances en premier pour profiter du cache
COPY pyproject.toml poetry.lock* /app/

# Copier tout le code du projet
COPY . /app/

# Installer les dépendances
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Exposer le port utilisé par uvicorn
EXPOSE 8000

# Commande de démarrage (mode dev pour commencer)
CMD ["uvicorn", "auth_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
