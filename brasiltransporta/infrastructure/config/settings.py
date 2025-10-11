# brasiltransporta/infrastructure/config/settings.py
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class AuthSettings(BaseSettings):
    """Configurações específicas para autenticação"""
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    bcrypt_rounds: int = 12

    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
        env_file=".env",
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
        env_file=".env",
        extra="ignore",
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
        env_file=".env",
        extra="ignore",
        env_aliases={
            "url": ["REDIS_URL", "redis_url"],
            "refresh_token_db": ["REDIS_REFRESH_TOKEN_DB"],
            "refresh_token_ttl": ["REDIS_REFRESH_TOKEN_TTL"],
            "refresh_token_namespace": ["REDIS_REFRESH_TOKEN_NAMESPACE"],
        },
        case_sensitive=False,
    )


class S3Settings(BaseSettings):
    """Configurações do Amazon S3"""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "sa-east-1"
    s3_bucket_name: str = "brasiltransporta-uploads"
    max_file_size_images: int = 5242880  # 5MB
    max_file_size_videos: int = 52428800  # 50MB
    max_images_per_ad: int = 10
    max_videos_per_ad: int = 3

    model_config = SettingsConfigDict(
        env_prefix="AWS_",
        env_file=".env",
        extra="ignore",
        env_aliases={
            "aws_access_key_id": ["AWS_ACCESS_KEY_ID"],
            "aws_secret_access_key": ["AWS_SECRET_ACCESS_KEY"],
            "aws_region": ["AWS_REGION"],
            "s3_bucket_name": ["S3_BUCKET_NAME"],
            "max_file_size_images": ["MAX_FILE_SIZE_IMAGES"],
            "max_file_size_videos": ["MAX_FILE_SIZE_VIDEOS"],
            "max_images_per_ad": ["MAX_IMAGES_PER_AD"],
            "max_videos_per_ad": ["MAX_VIDEOS_PER_AD"],
        },
        case_sensitive=False,
    )


class AppSettings(BaseSettings):
    """Configurações principais da aplicação usando Pydantic"""
    environment: str = "development"
    debug: bool = True

    # Sub-configs - usando Field com default_factory para evitar problemas de mutabilidade
    auth: AuthSettings = Field(default_factory=AuthSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    s3: S3Settings = Field(default_factory=S3Settings)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )


# Instância global das configurações
settings = AppSettings()