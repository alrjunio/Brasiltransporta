from pydantic import BaseModel, Field
from typing import Optional


class PresignedUrlRequest(BaseModel):
    """Modelo de request para geração de URL assinada"""
    
    file_key: str = Field(
        ...,
        description="Chave do arquivo no S3 (ex: ads/123/images/photo.jpg)",
        example="ads/123/images/photo.jpg"
    )
    
    operation: str = Field(
        default="get_object",
        description="Operação: 'get_object' (download) ou 'put_object' (upload)",
        example="get_object"
    )
    
    expires_in: int = Field(
        default=3600,
        description="Tempo de expiração em segundos (1 hora padrão)",
        ge=60,  # mínimo 1 minuto
        le=86400,  # máximo 24 horas
        example=3600
    )
    
    class Config:
        schema_extra = {
            "example": {
                "file_key": "ads/123/images/photo.jpg",
                "operation": "get_object",
                "expires_in": 3600
            }
        }


class BatchUploadRequest(BaseModel):
    """Modelo de request para upload em lote"""
    
    ad_id: str = Field(
        ...,
        description="ID do anúncio",
        example="550e8400-e29b-41d4-a716-446655440000"
    )
    
    file_keys: list[str] = Field(
        ...,
        description="Lista de chaves de arquivo para gerar URLs de upload",
        example=["ads/123/images/photo1.jpg", "ads/123/images/photo2.jpg"]
    )
    
    expires_in: int = Field(
        default=3600,
        description="Tempo de expiração das URLs em segundos",
        ge=300,  # mínimo 5 minutos para uploads
        le=7200,  # máximo 2 horas
        example=3600
    )
    
    class Config:
        schema_extra = {
            "example": {
                "ad_id": "550e8400-e29b-41d4-a716-446655440000",
                "file_keys": [
                    "ads/123/images/photo1.jpg",
                    "ads/123/images/photo2.jpg"
                ],
                "expires_in": 3600
            }
        }