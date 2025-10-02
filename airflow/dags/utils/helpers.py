import os
from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
from pathlib import Path
import random, re

# load environnment 
load_dotenv()

# minio variables
MINIO_ENDPOINT = "minio:9000"
MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
MINIO_SECRET_KEY  = os.getenv("MINIO_ROOT_PASSWORD")
BUCKET_NAME = "diabetes"

BASE_PATH = Path("/opt/airflow/data")


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
        
def download_from_minio(bucket_name, minio_path, local_file, client=None):
    if client is None:
        client = get_minio_client()
        
    try:
        client.fget_object(bucket_name, minio_path, local_file)
        print(f"✅ Fichier {local_file} téléchargé depuis MinIO → {bucket_name}/{minio_path}")
    except S3Error as e:
        print(f"❌ Erreur lors du téléchargement : {e}")

def prepare_path(base, subdir, filename):
    path = BASE_PATH / base / subdir
    path.mkdir(parents=True, exist_ok=True)
    return path / filename

def random_age_from_interval(interval):
    match = re.match(r'\[(\d+)-(\d+)\)', interval)
    if match:
        start = int(match.group(1))
        end = int(match.group(2))
        return random.randint(start, end - 1)
    else:
        return None
    
# def get_postgresql_engine(user: str = None, password: str=None, host: str=None, port: int=5432, db_name: str=None) -> Engine:
#     user = user or os.getenv("POSTGRES_USER", "postgres")
#     password = password or os.getenv("POSTGRES_PASSWORD", "postgres")
#     host = host or "postgres"
#     port = port or int(os.getenv("POSTGRES_HOST_PORT", 5432))
#     db_name = db_name or os.getenv("POSTGRES_DB_DW", "postgres")

#     connection_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
#     return create_engine(connection_string)