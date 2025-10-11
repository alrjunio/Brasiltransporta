from dataclasses import dataclass
from typing import Optional


from brasiltransporta.application.storage.services.file_storage_service import FileStorageInterface


@dataclass
class DeleteFileRequest:
    """DTO para requisição de deleção"""
    file_key: str


@dataclass
class DeleteFileResponse:
    """DTO para resposta de deleção"""
    success: bool
    error_message: Optional[str] = None


class DeleteFileUseCase:
    """Use Case para deleção de arquivos"""
    
    def __init__(self, file_storage: FileStorageInterface):
        self.file_storage = file_storage
    
    def execute(self, request: DeleteFileRequest) -> DeleteFileResponse:
        """
        Executa a deleção de um arquivo
        
        Args:
            request: Dados do arquivo para deletar
            
        Returns:
            DeleteFileResponse: Resultado da deleção
        """
        try:
            if not request.file_key:
                return DeleteFileResponse(
                    success=False,
                    error_message="Chave do arquivo não informada"
                )
            
            # Executa a deleção
            success = self.file_storage.delete_file(request.file_key)
            
            if success:
                return DeleteFileResponse(success=True)
            else:
                return DeleteFileResponse(
                    success=False,
                    error_message="Falha ao deletar arquivo do storage"
                )
                
        except Exception as e:
            return DeleteFileResponse(
                success=False,
                error_message=f"Erro inesperado na deleção: {str(e)}"
            )