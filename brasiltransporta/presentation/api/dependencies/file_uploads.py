from fastapi import Depends
from brasiltransporta.infrastructure.external.storage.storage_config import S3Config
from brasiltransporta.infrastructure.external.storage.s3_client import S3Client
from brasiltransporta.infrastructure.external.storage.file_validator import FileValidator
from brasiltransporta.application.storage.services.file_storage_service import S3FileStorageService
from brasiltransporta.application.storage.use_cases.upload_file import UploadFileUseCase
from brasiltransporta.application.storage.use_cases.delete_file import DeleteFileUseCase
from brasiltransporta.application.storage.use_cases.generate_presigned_url import GeneratePresignedUrlUseCase


def get_s3_config() -> S3Config:
    """Retorna configuração do S3 a partir de variáveis de ambiente"""
    return S3Config.from_env()


def get_s3_client(config: S3Config = Depends(get_s3_config)) -> S3Client:
    """Retorna cliente S3 configurado"""
    return S3Client(config)


def get_file_validator() -> FileValidator:
    """Retorna validador de arquivos"""
    return FileValidator()


def get_file_storage_service(
    s3_client: S3Client = Depends(get_s3_client),
    config: S3Config = Depends(get_s3_config)
) -> S3FileStorageService:
    """Retorna serviço de storage configurado"""
    return S3FileStorageService(config)


def get_upload_use_case(
    storage_service: S3FileStorageService = Depends(get_file_storage_service),
    validator: FileValidator = Depends(get_file_validator)
) -> UploadFileUseCase:
    """Retorna use case de upload configurado"""
    return UploadFileUseCase(storage_service, validator)


def get_delete_use_case(
    storage_service: S3FileStorageService = Depends(get_file_storage_service)
) -> DeleteFileUseCase:
    """Retorna use case de deleção configurado"""
    return DeleteFileUseCase(storage_service)


def get_presigned_url_use_case(
    storage_service: S3FileStorageService = Depends(get_file_storage_service)
) -> GeneratePresignedUrlUseCase:
    """Retorna use case de URL assinada configurado"""
    return GeneratePresignedUrlUseCase(storage_service)