"""
Módulo de storage da camada de aplicação
"""

from brasiltransporta.application.storage.services.file_storage_service import (
    FileStorageInterface,
    S3FileStorageService,
    UploadResult,
    PresignedUrlResult
)

from brasiltransporta.application.storage.use_cases.upload_file import (
    UploadFileUseCase,
    UploadFileRequest, 
    UploadFileResponse
)

from brasiltransporta.application.storage.use_cases.delete_file import (
    DeleteFileUseCase,
    DeleteFileRequest,
    DeleteFileResponse
)

from brasiltransporta.application.storage.use_cases.generate_presigned_url import (
    GeneratePresignedUrlUseCase,
    GeneratePresignedUrlRequest,
    GeneratePresignedUrlResponse
)

__all__ = [
    # Services
    "FileStorageInterface",
    "S3FileStorageService", 
    "UploadResult",
    "PresignedUrlResult",
    
    # Use Cases - Upload
    "UploadFileUseCase",
    "UploadFileRequest",
    "UploadFileResponse",
    
    # Use Cases - Delete
    "DeleteFileUseCase", 
    "DeleteFileRequest",
    "DeleteFileResponse",
    
    # Use Cases - Presigned URL
    "GeneratePresignedUrlUseCase",
    "GeneratePresignedUrlRequest",
    "GeneratePresignedUrlResponse"
]