FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema - usar libpq-dev CORRETO
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY backend/ ./backend/

# Expor porta
EXPOSE 8000

# Definindo backend no PYTHONPATH
ENV PYTHONPATH=/app/backend

# Comando para rodar a aplicação
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
