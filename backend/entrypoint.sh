#!/bin/sh
set -e

# Aguarda o banco estar disponível
echo "Aguardando banco de dados..."
sleep 5

# Executa as migrações do banco de dados (com tratamento de erro)
echo "Executando migrações..."
poetry run alembic -c /fundsys_project/alembic.ini upgrade head || echo "Migrações falharam, continuando..."

# Inicia a aplicação com hot-reload
echo "Iniciando aplicação..."
exec poetry run uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --reload-dir /fundsys_project/app \
  --reload-dir /fundsys_project