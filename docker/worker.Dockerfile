FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY backend/ ./backend/

ENV PYTHONPATH=/app/backend

# Comando para rodar o worker Celery
CMD ["celery", "-A", "backend.app.worker.celery_app", "worker", "--loglevel=info"]
