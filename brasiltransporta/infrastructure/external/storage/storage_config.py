import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class S3Config:
    """Configurações para Amazon S3"""
    access_key_id: str
    secret_access_key: str
    region_name: str = "sa-east-1"
    bucket_name: str = "brasiltransporta-uploads"
    endpoint_url: Optional[str] = None  # Para LocalStack/testing
    
    # Timeouts
    connect_timeout: int = 10
    read_timeout: int = 30
    
    # Tamanhos máximos de arquivo (em bytes)
    max_image_size: int = 5 * 1024 * 1024  # 5MB
    max_video_size: int = 50 * 1024 * 1024  # 50MB
    
    @classmethod
    def from_env(cls) -> "S3Config":
        """Cria configuração a partir de variáveis de ambiente"""
        return cls(
            access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
            secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
            region_name=os.getenv("AWS_REGION", "sa-east-1"),
            bucket_name=os.getenv("S3_BUCKET_NAME", "brasiltransporta-uploads"),
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),  # Para desenvolvimento
        )


@dataclass 
class FileValidationConfig:
    """Configurações para validação de arquivos"""
    # Tipos MIME permitidos para imagens
    allowed_image_mimes = {
        "image/jpeg": "jpg",
        "image/jpg": "jpg", 
        "image/png": "png",
        "image/webp": "webp"
    }
    
    # Tipos MIME permitidos para vídeos
    allowed_video_mimes = {
        "video/mp4": "mp4",
        "video/quicktime": "mov",  # iOS
        "video/x-msvideo": "avi"
    }
    
    # Tamanhos máximos
    max_image_size: int = 5 * 1024 * 1024  # 5MB
    max_video_size: int = 50 * 1024 * 1024  # 50MB
    
    # Limites de quantidade
    max_images_per_ad: int = 10
    max_videos_per_ad: int = 3