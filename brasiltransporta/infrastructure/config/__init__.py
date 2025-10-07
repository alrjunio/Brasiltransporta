# brasiltransporta/infrastructure/config/__init__.py

# Não reexporte o objeto `settings` aqui para evitar ciclos de import.
# Exponha apenas as classes de configuração (opcional).
from .settings import AppSettings, AuthSettings, DatabaseSettings, RedisSettings

__all__ = [
    "AppSettings",
    "AuthSettings",
    "DatabaseSettings",
    "RedisSettings",
]
