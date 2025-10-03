import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Use a mesma URL que está no docker-compose (ou pegue do ambiente)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@postgres_db:5432/brasiltransporta",
)

# Engine SQLAlchemy 2.x
engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)

# Factory de sessão
SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
    future=True,
)

def get_session() -> Session:
    """Retorna uma sessão nova (cada chamada cria uma)."""
    return SessionLocal()

__all__ = ["engine", "SessionLocal", "get_session"]
