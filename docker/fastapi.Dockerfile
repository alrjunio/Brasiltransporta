# ===== Base =====
FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# dependências de sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# ===== Deps =====
FROM base AS deps
# Caso use Poetry:
# COPY pyproject.toml poetry.lock* ./
# RUN pip install --upgrade pip poetry && poetry config virtualenvs.create false && poetry install --only main

# Caso use requirements:
# (Se tiver requirements.txt / requirements-dev.txt, copie e instale)
COPY requirements*.txt* ./
RUN pip install --upgrade pip && \
    (test -f requirements.txt && pip install -r requirements.txt || true) && \
    (test -f requirements-dev.txt && pip install -r requirements-dev.txt || true)

# Fallback: instala mínimos para a app e para os testes se não houver arquivos de deps
RUN python - <<'PY'
import importlib.util, sys
# Se fastapi não veio por requirements/dev, instala pacotes mínimos
def installed(pkg):
    return importlib.util.find_spec(pkg) is not None
missing = []
if not installed("fastapi"): missing += ["fastapi[standard]"]
if not installed("httpx"): missing += ["httpx>=0.26,<0.28"]
if not installed("sqlalchemy"): missing += ["sqlalchemy>=2.0"]
if not installed("pytest"): missing += ["pytest"]
if missing:
    import subprocess; subprocess.check_call([sys.executable,"-m","pip","install",*missing])
PY

# ===== Runtime (app) =====
FROM deps AS runtime
WORKDIR /app
COPY . .
# Ajuste o path do app se necessário
EXPOSE 8000
CMD ["uvicorn", "brasiltransporta.presentation.api.app:app", "--host", "0.0.0.0", "--port", "8000"]

# ===== Test runner =====
FROM deps AS test
WORKDIR /app
COPY . .
# Rode pytest por padrão; o compose pode sobrescrever command
CMD ["pytest", "-q"]
