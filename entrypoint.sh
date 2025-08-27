#!/bin/sh
set -e

# Executa as migrações do banco de dados
poetry run alembic -c /fundsys_project/alembic.ini upgrade head

# Inicia a aplicação com hot-reload
exec poetry run uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --reload-dir /fundsys_project/app \
  --reload-dir /fundsys_project