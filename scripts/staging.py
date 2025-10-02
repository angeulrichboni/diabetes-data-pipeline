from utils import get_postgresql_engine
import pandas as pd
from sqlachemy import text


engine = get_postgresql_engine()

with engine.connect() as connection:
    # Creer schema staging s'il n'existe pas
    connection.execute("CREATE SCHEMA IF NOT EXISTS staging;")
    
    # Create table staging.diabetes_clean 
    connection.execute(text("""
        CREATE TABLE staging.diabetes_clean (
        race TEXT,
        gender TEXT,
        age TEXT,
        age_num INT,
        admission_type_id INT,
        discharge_disposition_id INT,
        admission_source_id INT,
        time_in_hospital INT,
        payer_code TEXT,
        medical_specialty TEXT,
        num_lab_procedures INT,
        num_procedures INT,
        num_medications INT,
        number_outpatient INT,
        number_emergency INT,
        number_inpatient INT,
        diag_1 TEXT,
        diag_2 TEXT,
        diag_3 TEXT,
        number_diagnoses INT,
        metformin TEXT,
        repaglinide TEXT,
        nateglinide TEXT,
        chlorpropamide TEXT,
        glimepiride TEXT,
        acetohexamide TEXT,
        glipizide TEXT,
        glyburide TEXT,
        tolbutamide TEXT,
        pioglitazone TEXT,
        rosiglitazone TEXT,
        acarbose TEXT,
        miglitol TEXT,
        troglitazone TEXT,
        tolazamide TEXT,
        examide TEXT,
        citoglipton TEXT,
        insulin TEXT,
        glyburide_metformin TEXT,
        glipizide_metformin TEXT,
        glimepiride_pioglitazone TEXT,
        metformin_rosiglitazone TEXT,
        metformin_pioglitazone TEXT,
        change TEXT,
        diabetesMed TEXT,
        readmitted TEXT
    );
    """))
    
    # recuperer les donnee
    data_path = "/home/datauser/Projects/diabetes_project/data/processed/diabetes_processed.csv"
    data = pd.read_csv(data_path)
    
    #charger dans la bd
    try:
        data.to_sql('diabetes_clean', con=connection, schema='staging', if_exists='replace', index=False)
        print("✅ Données chargées avec succès dans la table 'staging.diabetes_clean'.")
    except Exception as e:
        print(f"❌ Erreur lors du chargement des données : {e}")
    