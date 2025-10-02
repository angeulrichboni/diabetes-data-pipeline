from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


from utils.extract_transform import extract_data, transform_data
from utils.load_data import staging_db


default_args = {
    'owner' : "Ange BONI",
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'diabetes_dag',
    schedule_interval=None,
    start_date=datetime(2025,9,26),
    catchup=False,
    default_args=default_args,
    template_searchpath=['/opt/airflow/dags/sql']
) as dag:

    # create_staging = SQLExecuteQueryOperator(
    #     task_id="create_staging_objects",
    #     sql="staging_diabetes.sql",
    #     conn_id="postgres_dw"   
    # )
    
    task_extract = PythonOperator(
        task_id ="extract_data",
        python_callable=extract_data
    )
    
    task_transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data
    )
    
    task_staging_db = PythonOperator(
        task_id="staging_db",
        python_callable=staging_db,
        execution_timeout=timedelta(minutes=30)
    )
    
    task_load_dimensions = SQLExecuteQueryOperator(
        task_id="load_dimensions",
        conn_id="postgres_dw",
        sql="load_dimensions.sql"
    )
    
    task_analytics_db = SQLExecuteQueryOperator(
        task_id="load_analytics",
        conn_id="postgres_dw",
        sql="load_fact_admission.sql"
    )

    # Définir l'ordre des tâches qui doit commencer par la création des objets de staging et l'extraction des données
    task_extract >> task_transform >> task_staging_db >> task_load_dimensions >> task_analytics_db