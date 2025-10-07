# brasiltransporta/infrastructure/config/settings.py
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore


class AuthSettings(BaseSettings):
    """Configurações específicas para autenticação"""
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Security
    bcrypt_rounds: int = 12

    # Pydantic v2
    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
        env_file=None,          # evita capturar variáveis de outras seções
        extra="ignore",
        env_aliases={
            "secret_key": ["AUTH_SECRET_KEY", "SECRET_KEY"],
            "algorithm": ["AUTH_ALGORITHM"],
            "access_token_expire_minutes": ["AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"],
            "refresh_token_expire_days": ["AUTH_REFRESH_TOKEN_EXPIRE_DAYS"],
            "bcrypt_rounds": ["AUTH_BCRYPT_ROUNDS"],
        },
        case_sensitive=False,
    )


class DatabaseSettings(BaseSettings):
    """Configurações de banco de dados"""
    url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/brasiltransporta"
    echo: bool = False

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=None,
        extra="ignore",
        # Compatibilidade com nomes comuns/antigos
        env_aliases={
            "url": ["DB_URL", "DATABASE_URL"],
            "echo": ["DB_ECHO"],
        },
        case_sensitive=False,
    )


class RedisSettings(BaseSettings):
    """Configurações do Redis"""
    url: str = "redis://localhost:6379/0"
    refresh_token_db: int = 0
    refresh_token_ttl: int = 60 * 60 * 24 * 7  # 7 days em segundos
    refresh_token_namespace: str = "refresh_tokens"

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_file=None,
        extra="ignore",
        env_aliases={
            "url": ["REDIS_URL", "redis_url"],
            "refresh_token_db": ["REDIS_REFRESH_TOKEN_DB"],
            "refresh_token_ttl": ["REDIS_REFRESH_TOKEN_TTL"],
            "refresh_token_namespace": ["REDIS_REFRESH_TOKEN_NAMESPACE"],
        },
        case_sensitive=False,
    )


class AppSettings(BaseSettings):
    """Configurações principais da aplicação"""
    environment: str = "development"
    debug: bool = True

    # Sub-configs (quem lê .env é o AppSettings; os sub-settings não leem .env diretamente)
    auth: AuthSettings = AuthSettings()
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()