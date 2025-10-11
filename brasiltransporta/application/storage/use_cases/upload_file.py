from typing import Dict, Any, Optional
from dataclasses import dataclass

from brasiltransporta.application.storage.services.file_storage_service import (
    FileStorageInterface, 
    UploadResult
)
from brasiltransporta.infrastructure.external.storage.file_validator import FileValidator


@dataclass
class UploadFileRequest:
    """DTO para requisição de upload"""
    file_content: bytes
    filename: str
    mime_type: str
    ad_id: str
    file_type: str  # 'image' ou 'video'
    metadata: Optional[Dict[str, str]] = None


@dataclass  
class UploadFileResponse:
    """DTO para resposta de upload"""
    success: bool
    file_url: Optional[str] = None
    file_key: Optional[str] = None
    error_message: Optional[str] = None
    file_size: int = 0


class UploadFileUseCase:
    """Use Case para upload de arquivos"""
    
    def __init__(self, file_storage: FileStorageInterface, validator: FileValidator = None):
        self.file_storage = file_storage
        self.validator = validator or FileValidator()
    
    def execute(self, request: UploadFileRequest) -> UploadFileResponse:
        """
        Executa o upload de um arquivo
        
        Args:
            request: Dados do arquivo para upload
            
        Returns:
            UploadFileResponse: Resultado do upload
        """
        try:
            # Validações básicas
            if not request.file_content:
                return UploadFileResponse(
                    success=False,
                    error_message="Conteúdo do arquivo vazio"
                )
            
            if not request.filename:
                return UploadFileResponse(
                    success=False, 
                    error_message="Nome do arquivo não informado"
                )
            
            if not request.ad_id:
                return UploadFileResponse(
                    success=False,
                    error_message="ID do anúncio não informado"
                )
            
            # Executa upload baseado no tipo
            if request.file_type == "image":
                result = self.file_storage.upload_image(
                    file_content=request.file_content,
                    filename=request.filename,
                    mime_type=request.mime_type,
                    ad_id=request.ad_id,
                    metadata=request.metadata
                )
            elif request.file_type == "video":
                result = self.file_storage.upload_video(
                    file_content=request.file_content,
                    filename=request.filename,
                    mime_type=request.mime_type,
                    ad_id=request.ad_id, 
                    metadata=request.metadata
                )
            else:
                return UploadFileResponse(
                    success=False,
                    error_message=f"Tipo de arquivo inválido: {request.file_type}"
                )
            
            # Converte o resultado
            return UploadFileResponse(
                success=result.success,
                file_url=result.file_url,
                file_key=result.file_key,
                error_message=result.error_message,
                file_size=result.file_size
            )
            
        except Exception as e:
            return UploadFileResponse(
                success=False,
                error_message=f"Erro inesperado no upload: {str(e)}"
            )