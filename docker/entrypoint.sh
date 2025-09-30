#!/usr/bin/env sh
set -e

echo "[entrypoint] aguardando Postgres..."
python - <<'PY'
import os, time, sys
import psycopg2
url = os.environ.get("DATABASE_URL","")
# Alembic/psycopg2 aceitam 'postgresql://'
if url.startswith("postgresql+psycopg2://"):
    url = url.replace("postgresql+psycopg2://","postgresql://", 1)
for i in range(60):
    try:
        conn = psycopg2.connect(url)
        conn.close()
        sys.exit(0)
    except Exception:
        time.sleep(1)
print("Banco não respondeu a tempo", file=sys.stderr)
sys.exit(1)
PY

echo "[entrypoint] rodando migrações Alembic..."
alembic upgrade head || true

echo "[entrypoint] iniciando o comando da aplicação..."
exec "$@"
