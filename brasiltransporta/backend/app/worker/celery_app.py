from celery import Celery
from app.config import settings

# Criação da instância do Celery
celery_app = Celery(
    "brasiltransporta",  # Nome da aplicação Celery
    broker=settings.RABBITMQ_URL,  # Broker RabbitMQ
    backend=settings.REDIS_URL,    # Backend Redis para resultados
    include=["app.worker.tasks"]   # Caminho para os módulos de tasks
)

# Configurações do Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
)

# Dicas de uso no Docker:
# Para rodar o worker no container:
# docker-compose exec worker celery -A app.worker.celery_app.celery_app worker --loglevel=info
#
# Para rodar o beat (tarefas periódicas) no container:
# docker-compose exec worker celery -A app.worker.celery_app.celery_app beat --loglevel=info
