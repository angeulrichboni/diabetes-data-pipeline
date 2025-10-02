from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)

data_path = Path("/opt/airflow/data/processed/diabetes_cleaned.csv")
def staging_db():
    try:
        logger.info("🚀 Début du chargement des données dans la base de données.")
        
        if not data_path.exists():
            raise FileNotFoundError(f"❌ Le fichier {data_path} n'existe pas.")
        
        hook = PostgresHook(postgres_conn_id="postgres_dw")
        engine = hook.get_sqlalchemy_engine()
        
        with engine.begin() as connection:
            connection.execute("TRUNCATE TABLE staging.diabetes_clean;")
            
            for chunk in pd.read_csv(data_path, chunksize=5000):
                    chunk.columns = [col.lower().replace('-', '_') for col in chunk.columns]
                    logger.info(f"📦 Insertion d’un chunk de {len(chunk)} lignes...")
                    chunk.to_sql(
                        "diabetes_clean",
                        con=connection,
                        schema="staging",
                        if_exists="append",
                        index=False,
                        method='multi',
                        chunksize=1000
                    )

        logger.info("✅ Données chargées avec succès dans la base de données.")

    except Exception as e:
        logger.error(f"❌ Erreur lors du chargement des données dans la base : {e}", exc_info=True)
        
