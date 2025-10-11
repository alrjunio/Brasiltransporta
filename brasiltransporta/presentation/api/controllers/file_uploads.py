from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, status
from typing import List, Optional
import uuid

from brasiltransporta.application.storage.use_cases.upload_file import UploadFileUseCase, UploadFileRequest
from brasiltransporta.application.storage.use_cases.delete_file import DeleteFileUseCase, DeleteFileRequest
from brasiltransporta.application.storage.use_cases.generate_presigned_url import GeneratePresignedUrlUseCase, GeneratePresignedUrlRequest

from brasiltransporta.presentation.api.models.requests.file_uploads import (
    PresignedUrlRequest,
    BatchUploadRequest
)
from brasiltransporta.presentation.api.models.responses.file_uploads import (
    UploadResponse,
    PresignedUrlResponse,
    BatchUploadResponse,
    FileInfoResponse,
    ErrorResponse
)
from brasiltransporta.presentation.api.dependencies.file_uploads import (
    get_file_storage_service,
    get_upload_use_case,
    get_delete_use_case,
    get_presigned_url_use_case
)
from brasiltransporta.presentation.api.dependencies.authz import get_current_user


router = APIRouter(prefix="/api/v1/storage", tags=["storage"])


@router.post(
    "/ads/{ad_id}/images",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload de imagem para anúncio",
    description="Faz upload de uma imagem para um anúncio específico"
)
async def upload_ad_image(
    ad_id: str,
    file: UploadFile = File(..., description="Arquivo de imagem (JPEG, PNG, WebP) até 5MB"),
    current_user: dict = Depends(get_current_user),
    upload_use_case: UploadFileUseCase = Depends(get_upload_use_case)
) -> UploadResponse:
    """
    Upload de imagem para anúncio
    
    - **ad_id**: ID do anúncio
    - **file**: Arquivo de imagem (máx 5MB)
    - Retorna URL do arquivo upload
    """
    try:
        # Lê o conteúdo do arquivo
        file_content = await file.read()
        
        # Prepara a requisição
        request = UploadFileRequest(
            file_content=file_content,
            filename=file.filename,
            mime_type=file.content_type,
            ad_id=ad_id,
            file_type="image",
            metadata={
                "uploaded_by": current_user.get("user_id", "unknown"),
                "original_filename": file.filename
            }
        )
        
        # Executa o use case
        result = upload_use_case.execute(request)
        
        if result.success:
            return UploadResponse(
                success=True,
                file_url=result.file_url,
                file_key=result.file_key,
                file_size=result.file_size,
                message="Imagem upload com sucesso"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error_message
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno no upload: {str(e)}"
        )


@router.post(
    "/ads/{ad_id}/videos",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload de vídeo para anúncio",
    description="Faz upload de um vídeo para um anúncio específico"
)
async def upload_ad_video(
    ad_id: str,
    file: UploadFile = File(..., description="Arquivo de vídeo (MP4, MOV, AVI) até 50MB"),
    current_user: dict = Depends(get_current_user),
    upload_use_case: UploadFileUseCase = Depends(get_upload_use_case)
) -> UploadResponse:
    """
    Upload de vídeo para anúncio
    
    - **ad_id**: ID do anúncio
    - **file**: Arquivo de vídeo (máx 50MB)
    - Retorna URL do arquivo upload
    """
    try:
        # Lê o conteúdo do arquivo
        file_content = await file.read()
        
        # Prepara a requisição
        request = UploadFileRequest(
            file_content=file_content,
            filename=file.filename,
            mime_type=file.content_type,
            ad_id=ad_id,
            file_type="video",
            metadata={
                "uploaded_by": current_user.get("user_id", "unknown"),
                "original_filename": file.filename
            }
        )
        
        # Executa o use case
        result = upload_use_case.execute(request)
        
        if result.success:
            return UploadResponse(
                success=True,
                file_url=result.file_url,
                file_key=result.file_key,
                file_size=result.file_size,
                message="Vídeo upload com sucesso"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error_message
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno no upload: {str(e)}"
        )


@router.post(
    "/presigned-url",
    response_model=PresignedUrlResponse,
    summary="Gera URL assinada",
    description="Gera uma URL assinada para upload/download direto do frontend"
)
async def generate_presigned_url(
    request: PresignedUrlRequest,
    current_user: dict = Depends(get_current_user),
    presigned_use_case: GeneratePresignedUrlUseCase = Depends(get_presigned_url_use_case)
) -> PresignedUrlResponse:
    """
    Gera URL assinada para operação no S3
    
    - **file_key**: Chave do arquivo no S3
    - **operation**: 'get_object' (download) ou 'put_object' (upload)
    - **expires_in**: Tempo de expiração em segundos (padrão: 3600)
    - Retorna URL assinada temporária
    """
    try:
        # Prepara a requisição
        use_case_request = GeneratePresignedUrlRequest(
            file_key=request.file_key,
            operation=request.operation,
            expires_in=request.expires_in
        )
        
        # Executa o use case
        result = presigned_use_case.execute(use_case_request)
        
        if result.success:
            return PresignedUrlResponse(
                success=True,
                url=result.url,
                expires_in=request.expires_in,
                message="URL assinada gerada com sucesso"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error_message
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar URL assinada: {str(e)}"
        )


@router.delete(
    "/files/{file_key}",
    response_model=dict,
    summary="Deleta arquivo",
    description="Deleta um arquivo do storage"
)
async def delete_file(
    file_key: str,
    current_user: dict = Depends(get_current_user),
    delete_use_case: DeleteFileUseCase = Depends(get_delete_use_case)
) -> dict:
    """
    Deleta arquivo do storage
    
    - **file_key**: Chave do arquivo no S3
    - Retorna confirmação da deleção
    """
    try:
        # Prepara a requisição
        request = DeleteFileRequest(file_key=file_key)
        
        # Executa o use case
        result = delete_use_case.execute(request)
        
        if result.success:
            return {
                "success": True,
                "message": "Arquivo deletado com sucesso",
                "file_key": file_key
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.error_message
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar arquivo: {str(e)}"
        )


@router.get(
    "/ads/{ad_id}/files",
    response_model=List[FileInfoResponse],
    summary="Lista arquivos do anúncio",
    description="Retorna lista de todos os arquivos de um anúncio"
)
async def list_ad_files(
    ad_id: str,
    current_user: dict = Depends(get_current_user)
) -> List[FileInfoResponse]:
    """
    Lista arquivos de um anúncio
    
    - **ad_id**: ID do anúncio
    - Retorna lista de arquivos com URLs
    """
    # Nota: Esta é uma implementação simplificada
    # Em produção, precisaríamos de um serviço para listar arquivos do S3
    # Por enquanto retornamos lista vazia - será implementado posteriormente
    
    return []