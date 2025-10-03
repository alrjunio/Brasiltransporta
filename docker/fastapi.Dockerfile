FROM python:3.11-slim

WORKDIR /app

# Dependências nativas (psycopg2 precisa de libpq-dev)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o projeto inteiro (inclui brasiltransporta/, docker/, etc.)
COPY . /app

# Copia scripts de inicialização
COPY docker/entrypoint.sh /app/docker/entrypoint.sh
COPY docker/wait_for_db.py /app/docker/wait_for_db.py
RUN chmod +x /app/docker/entrypoint.sh

# Garantir que o pacote "brasiltransporta" seja resolvido como módulo
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "brasiltransporta.presentation.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
