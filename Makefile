.PHONY: help lint test run clean migrate reset-db up down logs build ps shell format

help:
	@echo "Commandes principales :"
	@echo "  make up         # Build et démarre la stack Docker"
	@echo "  make down       # Arrête et supprime containers & volumes"
	@echo "  make logs       # Logs temps réel Docker"
	@echo "  make build      # Rebuild les images Docker"
	@echo "  make ps         # Liste les containers Docker"
	@echo "  make shell      # Ouvre un shell dans le container auth"
	@echo ""
	@echo "Dev local :"
	@echo "  make lint       # Lint le code Python"
	@echo "  make test       # Lance tous les tests Pytest"
	@echo "  make run        # Démarre le serveur FastAPI en local"
	@echo "  make migrate    # Exécute les migrations Alembic"
	@echo "  make reset-db   # Réinitialise la base et applique les migrations"
	@echo "  make format     # Formate le code avec Black"
	@echo "  make clean      # Supprime les fichiers .pyc et __pycache__"

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f

build:
	docker compose build

ps:
	docker compose ps

shell:
	docker compose exec auth /bin/bash

lint:
	cd services/auth_service && poetry run flake8 auth_service

test:
	cd services/auth_service && poetry run pytest -q

run:
	cd services/auth_service && poetry run uvicorn auth_service.main:app --reload

migrate:
	cd services/auth_service && poetry run alembic upgrade head

reset-db:
        docker compose exec -T db psql -U $$POSTGRES_USER -d postgres -c "DROP DATABASE IF EXISTS $$POSTGRES_DB;"
	docker compose exec -T db psql -U $$POSTGRES_USER -d postgres -c "CREATE DATABASE $$POSTGRES_DB;"
	cd services/auth_service && poetry run alembic upgrade head

format:
	cd services/auth_service && poetry run black auth_service

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

