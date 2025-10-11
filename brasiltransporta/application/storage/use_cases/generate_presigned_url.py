from dataclasses import dataclass
from typing import Optional

from brasiltransporta.application.storage.services.file_storage_service import FileStorageInterface, PresignedUrlResult


@dataclass
class GeneratePresignedUrlRequest:
    """DTO para requisição de URL assinada"""
    file_key: str
    operation: str = "get_object"  # "get_object" ou "put_object"
    expires_in: int = 3600  # segundos


@dataclass
class GeneratePresignedUrlResponse:
    """DTO para resposta de URL assinada"""
    success: bool
    url: Optional[str] = None
    error_message: Optional[str] = None


class GeneratePresignedUrlUseCase:
    """Use Case para geração de URLs assinadas"""
    
    def __init__(self, file_storage: FileStorageInterface):
        self.file_storage = file_storage
    
    def execute(self, request: GeneratePresignedUrlRequest) -> GeneratePresignedUrlResponse:
        """
        Gera uma URL assinada para um arquivo
        
        Args:
            request: Dados para geração da URL
            
        Returns:
            GeneratePresignedUrlResponse: URL assinada ou erro
        """
        try:
            if not request.file_key:
                return GeneratePresignedUrlResponse(
                    success=False,
                    error_message="Chave do arquivo não informada"
                )
            
            # Valida operação
            if request.operation not in ["get_object", "put_object"]:
                return GeneratePresignedUrlResponse(
                    success=False,
                    error_message=f"Operação inválida: {request.operation}"
                )
            
            # Gera a URL assinada
            result = self.file_storage.generate_presigned_url(
                file_key=request.file_key,
                operation=request.operation,
                expires_in=request.expires_in
            )
            
            # Converte o resultado
            return GeneratePresignedUrlResponse(
                success=result.success,
                url=result.url,
                error_message=result.error_message
            )
            
        except Exception as e:
            return GeneratePresignedUrlResponse(
                success=False,
                error_message=f"Erro inesperado na geração de URL: {str(e)}"
            )