import os
from sqlalchemy import create_engine
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.base import Base

# importe todos os MODELS que devem criar tabela (pelo menos o UserModel neste slice)
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.user import UserModel  # noqa: F401

# Use a mesma URL do docker-compose (ou do seu .env)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@postgres_db:5432/brasiltransporta",
)

# Cria um engine próprio para este script (independente do session.py)
engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)


def main():
    Base.metadata.create_all(bind=engine)
    print("OK: tables created.")


if __name__ == "__main__":
    main()
