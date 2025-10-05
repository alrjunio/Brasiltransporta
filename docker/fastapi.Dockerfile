# ========= Base =========
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Dependências de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir -U pip

# ========= Deps =========
FROM base AS deps

# Copia arquivos de dependências
COPY pyproject.toml poetry.lock* ./
COPY requirements*.txt ./

# Instala dependências de forma otimizada - CORRIGIDO para Poetry 2.2.1
RUN --mount=type=cache,target=/root/.cache/pip \
    set -eux \
    && if [ -f "poetry.lock" ]; then \
        pip install --no-cache-dir poetry \
        && poetry install --without dev --no-interaction --no-ansi; \
    elif [ -f "requirements.txt" ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    else \
        echo "Instalando dependências mínimas..." \
        && pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary; \
    fi

# ========= Runtime =========
FROM deps AS runtime

COPY . /app

# Usuário não-root
RUN groupadd -r app && useradd -r -g app app \
    && chown -R app:app /app
USER app

EXPOSE 8000

CMD ["uvicorn", "brasiltransporta.presentation.api.app:app", "--host", "0.0.0.0", "--port", "8000"]

# ========= Test =========
FROM deps AS test

# Instala dependências de desenvolvimento - CORRIGIDO
RUN --mount=type=cache,target=/root/.cache/pip \
    set -eux \
    && pip install --no-cache-dir poetry \
    && poetry install --with dev --no-interaction --no-ansi

COPY . /app

RUN groupadd -r tester && useradd -r -g tester tester \
    && chown -R tester:tester /app
USER tester

CMD ["pytest", "-q", "--disable-warnings", "--timeout=30", "--durations=10"]