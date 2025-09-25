FROM python:3.11-slim

WORKDIR /app

# Instalar Poetry
RUN pip install --no-cache-dir poetry

# Copiar arquivos do Poetry
COPY app/pyproject.toml app/poetry.lock* /app/

# Instalar dependências sem criar venv
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copiar código
COPY app/ /app

# Comando padrão
CMD ["python", "main.py"]