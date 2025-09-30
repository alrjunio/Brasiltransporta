import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

# Carrega logging do alembic.ini (se houver)
config = context.config
if config.config_file_name is not None:
    try:
        fileConfig(config.config_file_name, disable_existing_loggers=False)
    except Exception:
        # Se faltar seções de logging no alembic.ini, seguimos sem configurar logging
        pass



def _database_url() -> str:
    """
    Prioriza DATABASE_URL. Se ausente, monta a URL a partir das variáveis
    do docker-compose: POSTGRES_* (com defaults sensatos).
    """
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "postgres_db")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "brasiltransporta")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


# ===== Metadata dos modelos do projeto =====
# Importa a Base e garante que os modelos sejam importados para popular o metadata.
from brasiltransporta.infrastructure.persistence.sqlalchemy.models.base import Base  # noqa: E402
# Importe todos os módulos de modelos aqui para o autogenerate "enxergar" as tabelas:
from brasiltransporta.infrastructure.persistence.sqlalchemy.models import user  # noqa: F401,E402

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Executa migrações em modo 'offline' (sem abrir conexão)."""
    url = _database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,              # detecta mudanças de tipo
        compare_server_default=True,    # detecta mudanças de default
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações em modo 'online' (com conexão ativa)."""
    connectable = create_engine(_database_url(), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            # include_schemas=False,  # ajuste se você usar múltiplos schemas
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
