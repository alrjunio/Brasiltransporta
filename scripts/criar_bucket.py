# criar_bucket.py
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

def criar_bucket_s3():
    print("🚀 Criando bucket S3...")
    
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
        bucket_name = os.getenv('S3_BUCKET_NAME')
        
        # Criar bucket
        if os.getenv('AWS_REGION') == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': os.getenv('AWS_REGION')}
            )
        
        print(f"✅ Bucket '{bucket_name}' criado com sucesso!")
        
        # Configurar para acesso público (apenas leitura)
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        
        print("✅ Configurações de acesso público aplicadas!")
        return True
        
    except Exception as e:
        if "BucketAlreadyExists" in str(e) or "BucketAlreadyOwnedByYou" in str(e):
            print(f"✅ Bucket '{bucket_name}' já existe!")
            return True
        else:
            print(f"❌ Erro ao criar bucket: {e}")
            return False

if __name__ == "__main__":
    criar_bucket_s3()