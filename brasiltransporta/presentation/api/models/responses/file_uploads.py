from pydantic import BaseModel, Field
from typing import Optional, List


class UploadResponse(BaseModel):
    """Modelo de response para upload de arquivo"""
    
    success: bool = Field(..., description="Indica se o upload foi bem sucedido")
    file_url: Optional[str] = Field(None, description="URL pública do arquivo")
    file_key: Optional[str] = Field(None, description="Chave interna do arquivo no S3")
    file_size: Optional[int] = Field(None, description="Tamanho do arquivo em bytes")
    message: Optional[str] = Field(None, description="Mensagem descritiva")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "file_url": "https://brasiltransporta-uploads.s3.sa-east-1.amazonaws.com/ads/123/images/photo.jpg",
                "file_key": "ads/123/images/photo.jpg",
                "file_size": 1024000,
                "message": "Imagem upload com sucesso"
            }
        }


class PresignedUrlResponse(BaseModel):
    """Modelo de response para URL assinada"""
    
    success: bool = Field(..., description="Indica se a geração foi bem sucedida")
    url: Optional[str] = Field(None, description="URL assinada gerada")
    expires_in: Optional[int] = Field(None, description="Tempo de expiração em segundos")
    message: Optional[str] = Field(None, description="Mensagem descritiva")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "url": "https://brasiltransporta-uploads.s3.sa-east-1.amazonaws.com/ads/123/images/photo.jpg?AWSAccessKeyId=...",
                "expires_in": 3600,
                "message": "URL assinada gerada com sucesso"
            }
        }


class FileInfoResponse(BaseModel):
    """Modelo de response para informações do arquivo"""
    
    file_key: str = Field(..., description="Chave do arquivo no S3")
    file_url: str = Field(..., description="URL pública do arquivo")
    file_type: str = Field(..., description="Tipo do arquivo: image ou video")
    file_size: int = Field(..., description="Tamanho do arquivo em bytes")
    uploaded_at: Optional[str] = Field(None, description="Data do upload")
    
    class Config:
        schema_extra = {
            "example": {
                "file_key": "ads/123/images/photo.jpg",
                "file_url": "https://brasiltransporta-uploads.s3.sa-east-1.amazonaws.com/ads/123/images/photo.jpg",
                "file_type": "image",
                "file_size": 1024000,
                "uploaded_at": "2024-01-15T10:30:00Z"
            }
        }


class BatchUploadResponse(BaseModel):
    """Modelo de response para upload em lote"""
    
    success: bool = Field(..., description="Indica se a operação foi bem sucedida")
    urls: List[PresignedUrlResponse] = Field(..., description="Lista de URLs assinadas geradas")
    message: Optional[str] = Field(None, description="Mensagem descritiva")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "urls": [
                    {
                        "success": True,
                        "url": "https://brasiltransporta-uploads.s3.sa-east-1.amazonaws.com/ads/123/images/photo1.jpg?AWSAccessKeyId=...",
                        "expires_in": 3600,
                        "message": "URL assinada gerada com sucesso"
                    }
                ],
                "message": "URLs assinadas geradas com sucesso"
            }
        }


class ErrorResponse(BaseModel):
    """Modelo de response para erros"""
    
    success: bool = Field(..., description="Sempre false para erros")
    error: str = Field(..., description="Mensagem de erro")
    details: Optional[dict] = Field(None, description="Detalhes adicionais do erro")
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error": "Arquivo muito grande",
                "details": {"max_size": 5242880, "actual_size": 10485760}
            }
        }