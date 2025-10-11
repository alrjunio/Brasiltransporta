from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from brasiltransporta.infrastructure.external.storage.s3_client import S3Client
from brasiltransporta.infrastructure.external.storage.file_validator import FileValidator
from brasiltransporta.infrastructure.external.storage.storage_config import S3Config, FileValidationConfig


@dataclass
class UploadResult:
    """Resultado de uma operação de upload"""
    success: bool
    file_url: Optional[str] = None
    file_key: Optional[str] = None
    error_message: Optional[str] = None
    file_size: int = 0


@dataclass
class PresignedUrlResult:
    """Resultado de geração de URL assinada"""
    success: bool
    url: Optional[str] = None
    error_message: Optional[str] = None


class FileStorageInterface(ABC):
    """Interface para serviços de armazenamento de arquivos"""
    
    @abstractmethod
    def upload_image(
        self, 
        file_content: bytes, 
        filename: str, 
        mime_type: str,
        ad_id: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> UploadResult:
        """Faz upload de imagem para um anúncio"""
        pass
    
    @abstractmethod
    def upload_video(
        self,
        file_content: bytes,
        filename: str,
        mime_type: str, 
        ad_id: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> UploadResult:
        """Faz upload de vídeo para um anúncio"""
        pass
    
    @abstractmethod
    def generate_presigned_url(
        self,
        file_key: str,
        operation: str = "get_object",
        expires_in: int = 3600
    ) -> PresignedUrlResult:
        """Gera URL assinada para um arquivo"""
        pass
    
    @abstractmethod
    def delete_file(self, file_key: str) -> bool:
        """Deleta arquivo do storage"""
        pass
    
    @abstractmethod
    def get_file_url(self, file_key: str) -> Optional[str]:
        """Obtém URL pública do arquivo"""
        pass


class S3FileStorageService(FileStorageInterface):
    """Implementação do serviço de storage usando Amazon S3"""
    
    def __init__(self, s3_config: S3Config, validation_config: FileValidationConfig = None):
        self.s3_client = S3Client(s3_config)
        self.validator = FileValidator(validation_config)
        self.bucket_name = s3_config.bucket_name
        self.region = s3_config.region_name
    
    def upload_image(
        self, 
        file_content: bytes, 
        filename: str, 
        mime_type: str,
        ad_id: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> UploadResult:
        """Faz upload de imagem para um anúncio"""
        try:
            # Valida o arquivo
            is_valid, error_msg = self.validator.validate_image(file_content, filename, mime_type)
            if not is_valid:
                return UploadResult(success=False, error_message=error_msg)
            
            # Gera a chave S3
            file_extension = filename.split('.')[-1].lower()
            s3_key = f"ads/{ad_id}/images/{filename}"
            
            # Adiciona metadados padrão
            file_metadata = metadata or {}
            file_metadata.update({
                "ad_id": ad_id,
                "file_type": "image",
                "original_filename": filename
            })
            
            # Faz upload
            upload_success = self.s3_client.upload_file(
                file_content, s3_key, file_metadata
            )
            
            if upload_success:
                file_url = self.get_file_url(s3_key)
                return UploadResult(
                    success=True,
                    file_url=file_url,
                    file_key=s3_key,
                    file_size=len(file_content)
                )
            else:
                return UploadResult(
                    success=False, 
                    error_message="Falha no upload para S3"
                )
                
        except Exception as e:
            return UploadResult(
                success=False,
                error_message=f"Erro inesperado no upload: {str(e)}"
            )
    
    def upload_video(
        self,
        file_content: bytes,
        filename: str,
        mime_type: str, 
        ad_id: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> UploadResult:
        """Faz upload de vídeo para um anúncio"""
        try:
            # Valida o arquivo
            is_valid, error_msg = self.validator.validate_video(file_content, filename, mime_type)
            if not is_valid:
                return UploadResult(success=False, error_message=error_msg)
            
            # Gera a chave S3
            file_extension = filename.split('.')[-1].lower()
            s3_key = f"ads/{ad_id}/videos/{filename}"
            
            # Adiciona metadados padrão
            file_metadata = metadata or {}
            file_metadata.update({
                "ad_id": ad_id,
                "file_type": "video", 
                "original_filename": filename
            })
            
            # Faz upload
            upload_success = self.s3_client.upload_file(
                file_content, s3_key, file_metadata
            )
            
            if upload_success:
                file_url = self.get_file_url(s3_key)
                return UploadResult(
                    success=True,
                    file_url=file_url,
                    file_key=s3_key, 
                    file_size=len(file_content)
                )
            else:
                return UploadResult(
                    success=False,
                    error_message="Falha no upload para S3"
                )
                
        except Exception as e:
            return UploadResult(
                success=False,
                error_message=f"Erro inesperado no upload: {str(e)}"
            )
    
    def generate_presigned_url(
        self,
        file_key: str,
        operation: str = "get_object",
        expires_in: int = 3600
    ) -> PresignedUrlResult:
        """Gera URL assinada para um arquivo"""
        try:
            url = self.s3_client.generate_presigned_url(
                file_key, operation, expires_in
            )
            
            if url:
                return PresignedUrlResult(success=True, url=url)
            else:
                return PresignedUrlResult(
                    success=False,
                    error_message="Falha ao gerar URL assinada"
                )
                
        except Exception as e:
            return PresignedUrlResult(
                success=False,
                error_message=f"Erro ao gerar URL assinada: {str(e)}"
            )
    
    def delete_file(self, file_key: str) -> bool:
        """Deleta arquivo do storage"""
        try:
            return self.s3_client.delete_file(file_key)
        except Exception as e:
            # Log do erro mas não quebra a aplicação
            print(f"Erro ao deletar arquivo {file_key}: {str(e)}")
            return False
    
    def get_file_url(self, file_key: str) -> Optional[str]:
        """Obtém URL pública do arquivo"""
        try:
            # Para S3, a URL pública segue este formato
            return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{file_key}"
        except Exception:
            return None