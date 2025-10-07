FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir -U pip

COPY pyproject.toml poetry.lock* ./
COPY requirements*.txt ./

RUN --mount=type=cache,target=/root/.cache/pip \
    set -eux \
    && if [ -f "poetry.lock" ]; then \
        pip install --no-cache-dir poetry \
        && poetry install --no-interaction --no-ansi; \
    elif [ -f "requirements.txt" ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    else \
        pip install --no-cache-dir celery redis psycopg2-binary; \
    fi

COPY . /app

RUN groupadd -r worker && useradd -r -g worker worker \
    && chown -R worker:worker /app
USER worker

CMD ["celery", "-A", "brasiltransporta.worker.celery_app", "worker", "--loglevel=info"]
