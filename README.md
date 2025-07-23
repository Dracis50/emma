# EMMA Auth-Service

Micro-service d’authentification (FastAPI + JWT) destiné au projet **EMMA**.

```bash
# Lancer en local
cp .env.example .env    # puis remplis les variables
docker compose up -d --build	  •	https://auth.${DOMAIN}/healthz → check de vie
	•	https://auth.${DOMAIN}/api/v1/… → endpoints REST
