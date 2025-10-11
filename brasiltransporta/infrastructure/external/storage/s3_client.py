import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional, Dict, Any
import logging

from brasiltransporta.infrastructure.external.storage.storage_config import S3Config


logger = logging.getLogger(__name__)


class S3Client:
    """Cliente para interação com Amazon S3"""
    
    def __init__(self, config: S3Config):
        self.config = config
        self._client = None
    
    @property
    def client(self):
        """Lazy initialization do cliente S3"""
        if self._client is None:
            try:
                self._client = boto3.client(
                    's3',
                    aws_access_key_id=self.config.access_key_id,
                    aws_secret_access_key=self.config.secret_access_key,
                    region_name=self.config.region_name,
                    endpoint_url=self.config.endpoint_url,
                    config=boto3.session.Config(
                        connect_timeout=self.config.connect_timeout,
                        read_timeout=self.config.read_timeout,
                        retries={'max_attempts': 3}
                    )
                )
                logger.info("Cliente S3 inicializado com sucesso")
            except NoCredentialsError:
                logger.error("Credenciais AWS não encontradas")
                raise
            except Exception as e:
                logger.error(f"Erro ao inicializar cliente S3: {str(e)}")
                raise
        return self._client
    
    def upload_file(
        self, 
        file_content: bytes, 
        s3_key: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        Faz upload de arquivo para S3
        
        Args:
            file_content: Conteúdo do arquivo em bytes
            s3_key: Chave do arquivo no S3
            metadata: Metadados opcionais
            
        Returns:
            bool: True se upload foi bem sucedido
        """
        try:
            self.client.put_object(
                Bucket=self.config.bucket_name,
                Key=s3_key,
                Body=file_content,
                Metadata=metadata or {},
                ContentType=self._detect_content_type(s3_key)
            )
            logger.info(f"Arquivo {s3_key} upload com sucesso")
            return True
            
        except ClientError as e:
            logger.error(f"Erro no upload para S3: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Erro inesperado no upload: {str(e)}")
            return False
    
    def generate_presigned_url(
        self, 
        s3_key: str, 
        operation: str = "get_object",
        expires_in: int = 3600
    ) -> Optional[str]:
        """
        Gera URL assinada para operação no S3
        
        Args:
            s3_key: Chave do arquivo
            operation: Operação ('get_object', 'put_object')
            expires_in: Tempo de expiração em segundos
            
        Returns:
            str: URL assinada ou None em caso de erro
        """
        try:
            url = self.client.generate_presigned_url(
                operation,
                Params={
                    'Bucket': self.config.bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            logger.error(f"Erro ao gerar URL assinada: {str(e)}")
            return None
    
    def delete_file(self, s3_key: str) -> bool:
        """
        Deleta arquivo do S3
        
        Args:
            s3_key: Chave do arquivo
            
        Returns:
            bool: True se deleção foi bem sucedida
        """
        try:
            self.client.delete_object(
                Bucket=self.config.bucket_name,
                Key=s3_key
            )
            logger.info(f"Arquivo {s3_key} deletado com sucesso")
            return True
        except ClientError as e:
            logger.error(f"Erro ao deletar arquivo do S3: {str(e)}")
            return False
    
    def _detect_content_type(self, filename: str) -> str:
        """Detecta content type baseado na extensão do arquivo"""
        extension = filename.lower().split('.')[-1]
        content_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'webp': 'image/webp',
            'mp4': 'video/mp4',
            'mov': 'video/quicktime',
            'avi': 'video/x-msvideo'
        }
        return content_types.get(extension, 'application/octet-stream')