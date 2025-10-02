from pathlib import Path
import random, re
from sqlachemy import create_engine
from sqlachemy.engine import Engine
import os

def prepare_path(*path_parts):
    """
    Construit un chemin à partir des arguments et crée le dossier parent si nécessaire.

    Usage :
        output_path = prepare_path("data", "raw", "diabetes.csv")
    """ 
    path = Path(*path_parts).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def random_age_from_interval(interval):
    match = re.match(r'\[(\d+)-(\d+)\)', interval)
    if match:
        start = int(match.group(1))
        end = int(match.group(2))
        return random.randint(start, end - 1)
    else:
        return None
    
def get_postgresql_engine(user: str = None, password: str=None, host: str=None, port: int=5432, db_name: str=None) -> Engine:
    user = user or os.getenv("POSTGRES_USER", "postgres")
    password = password or os.getenv("POSTGRES_PASSWORD", "postgres")
    host = host or os.getenv("POSTGRES_HOST", "localhost")
    port = port or int(os.getenv("POSTGRES_HOST_PORT", 5432))
    db_name = db_name or os.getenv("POSTGRES_DB_DW", "postgres")

    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    return create_engine(connection_string)