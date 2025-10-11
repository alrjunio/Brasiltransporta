"""
Módulo de storage para integração com Amazon S3
"""

from brasiltransporta.infrastructure.external.storage.s3_client import S3Client
from brasiltransporta.infrastructure.external.storage.file_validator import FileValidator, FileValidationError
from brasiltransporta.infrastructure.external.storage.storage_config import S3Config, FileValidationConfig

__all__ = [
    "S3Client",
    "FileValidator", 
    "FileValidationError",
    "S3Config",
    "FileValidationConfig"
]