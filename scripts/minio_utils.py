import os
from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv

# load environnment 
load_dotenv()

# minio variables
MINIO_ENDPOINT = "localhost:5001"
MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
MINIO_SECRET_KEY  = os.getenv("MINIO_ROOT_PASSWORD")
BUCKET_NAME = "diabetes"


def get_minio_client():
    if not MINIO_ACCESS_KEY or not MINIO_SECRET_KEY:
        raise ValueError("❌ Les variables MINIO_ROOT_USER et MINIO_ROOT_PASSWORD ne sont pas définies.")
    
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )
    
    return client

def upload_to_minio(local_file, bucket_name, minio_path, client=None):
    if client is None:
        client = get_minio_client()
        
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"✅ Bucket '{bucket_name}' créé.")
    else:
        print(f"ℹ️ Bucket '{bucket_name}' déjà existant.")
        
    try:
        client.fput_object(bucket_name, minio_path, local_file)
        print(f"✅ Fichier {local_file} uploadé dans MinIO → {bucket_name}/{minio_path}")
    except S3Error as e:
        print(f"❌ Erreur lors de l'upload : {e}")
