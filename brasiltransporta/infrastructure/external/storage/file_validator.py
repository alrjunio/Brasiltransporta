import os
from typing import Dict, List, Tuple
from dataclasses import dataclass
from brasiltransporta.infrastructure.external.storage.storage_config import FileValidationConfig


class FileValidationError(Exception):
    """Exceção para erros de validação de arquivo"""
    pass


class FileValidator:
    """Validador de arquivos para upload"""
    
    def __init__(self, config: FileValidationConfig = None):
        self.config = config or FileValidationConfig()
    
    def validate_image(self, file_content: bytes, filename: str, mime_type: str) -> Tuple[bool, str]:
        """
        Valida um arquivo de imagem
        
        Args:
            file_content: Conteúdo do arquivo em bytes
            filename: Nome do arquivo
            mime_type: Tipo MIME do arquivo
            
        Returns:
            Tuple[bool, str]: (sucesso, mensagem_erro)
        """
        try:
            # Valida tipo MIME
            if mime_type not in self.config.allowed_image_mimes:
                allowed = ", ".join(self.config.allowed_image_mimes.keys())
                return False, f"Tipo de arquivo não permitido. Tipos aceitos: {allowed}"
            
            # Valida tamanho
            if len(file_content) > self.config.max_image_size:
                max_mb = self.config.max_image_size / (1024 * 1024)
                return False, f"Arquivo muito grande. Tamanho máximo: {max_mb}MB"
            
            # Valida extensão
            _, ext = os.path.splitext(filename)
            if ext.lower() not in ['.jpg', '.jpeg', '.png', '.webp']:
                return False, "Extensão de arquivo não permitida para imagens"
            
            return True, "Arquivo válido"
            
        except Exception as e:
            return False, f"Erro na validação: {str(e)}"
    
    def validate_video(self, file_content: bytes, filename: str, mime_type: str) -> Tuple[bool, str]:
        """
        Valida um arquivo de vídeo
        """
        try:
            # Valida tipo MIME
            if mime_type not in self.config.allowed_video_mimes:
                allowed = ", ".join(self.config.allowed_video_mimes.keys())
                return False, f"Tipo de arquivo não permitido. Tipos aceitos: {allowed}"
            
            # Valida tamanho
            if len(file_content) > self.config.max_video_size:
                max_mb = self.config.max_video_size / (1024 * 1024)
                return False, f"Arquivo muito grande. Tamanho máximo: {max_mb}MB"
            
            # Valida extensão
            _, ext = os.path.splitext(filename)
            if ext.lower() not in ['.mp4', '.mov', '.avi']:
                return False, "Extensão de arquiva não permitida para vídeos"
            
            return True, "Arquivo válido"
            
        except Exception as e:
            return False, f"Erro na validação: {str(e)}"
    
    def validate_quantity(self, current_count: int, file_type: str, operation: str = "add") -> Tuple[bool, str]:
        """
        Valida quantidade de arquivos por anúncio
        
        Args:
            current_count: Quantidade atual de arquivos
            file_type: 'image' ou 'video'
            operation: 'add' ou 'set'
        """
        try:
            if file_type == "image":
                max_count = self.config.max_images_per_ad
            elif file_type == "video":
                max_count = self.config.max_videos_per_ad
            else:
                return False, "Tipo de arquivo inválido"
            
            if operation == "add" and current_count >= max_count:
                return False, f"Máximo de {max_count} {file_type}s por anúncio atingido"
            
            if operation == "set" and current_count > max_count:
                return False, f"Máximo de {max_count} {file_type}s por anúncio excedido"
            
            return True, "Quantidade válida"
            
        except Exception as e:
            return False, f"Erro na validação de quantidade: {str(e)}"