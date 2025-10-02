from ucimlrepo import fetch_ucirepo
from utils.helpers import upload_to_minio, random_age_from_interval, prepare_path
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def extract_data():
    logger.info("📥 Starting data extraction from UCI repository")
    output_path = prepare_path("data", "raw", "diabetes.csv")

    # fetch dataset
    diabetes_130_us_hospitals_for_years_1999_2008 = fetch_ucirepo(id=296)

    # data (as pandas dataframes) 
    X = diabetes_130_us_hospitals_for_years_1999_2008.data.features 
    y = diabetes_130_us_hospitals_for_years_1999_2008.data.targets 
    
    # Create dataset
    data = X.copy()
    data["readmitted"] = y["readmitted"]

    # upload to minio
    data.to_csv(output_path, index=False)
    upload_to_minio(str(output_path), "diabetes", "raw/diabetes.csv")
    logger.info("✅ Data uploaded to MinIO")
    
def transform_data():
    logger.info("🔧 Starting data transformation")
    input_path = prepare_path("data", "raw", "diabetes.csv")
    output_path = prepare_path("data", "processed", "diabetes_cleaned.csv")

    # load data
    data = pd.read_csv(input_path)

    # Supprimer les colonnes dont le % de valeurs manquantes est supérieur à un seuil
    missing_percent = data.isnull().mean() * 100
    threshold = 80.0  # Seuil en pourcentage
    cols_to_drop = [col for col, val in missing_percent.items() if val > threshold]
    data.drop(columns=cols_to_drop, inplace=True)

    # Remplacer les valeurs manquantes dans les colonnes object par Unknown
    data_object_with_NAN = ['race', 'payer_code', 'medical_specialty', 'diag_1', 'diag_2', 'diag_3']
    for col in data_object_with_NAN:
        data[col] = data[col].fillna('Unknown')
        
    # Nettoyer les colonnes de type object : enlever les espaces, mettre en minuscule, remplacer les espaces par des underscores
    object_cols = data.select_dtypes(include=['object']).columns
    for col in object_cols:
        data[col] = data[col].str.strip().str.lower().str.replace(' ', '_')
        
    # Voir les valeurs uniques de race puis les uniformiser    
    data['race'] = data['race'].replace({
        'africanamerican': 'african american',
        'unknown': 'unknown',
        'other': 'other',
        'caucasian': 'caucasian',
        'asian': 'asian',
        'hispanic': 'hispanic'
    })

    # Creer une colonne age_num avec un âge aléatoire dans l'intervalle donné dans la colonne age
    data['age_num'] = data['age'].apply(random_age_from_interval)

    # Nettoyer la colonne medical_specialty
    corrections = {
        'obstetricsandgynecology': 'obstetrics-gynecology',
        'surgery-plasticwithinheadandneck': 'surgery-plastic-within-head-and-neck',
        'pediatrics-emergencymedicine': 'pediatrics-emergency-medicine',
        'physicalmedicineandrehabilitation': 'physical-medicine-and-rehabilitation',
        'allergyandimmunology': 'allergy-and-immunology',
        'pediatrics-infectiousdiseases': 'pediatrics-infectious-diseases',
        'pediatrics-allergyandimmunology': 'pediatrics-allergy-and-immunology',
        'physiciannotfound': "unknown",  
        'surgicalspecialty': "unknown",  
        'dcpteam': "unknown",
        'resident': "unknown",
        'surgeon': "unknown",
        'outreachservices': "unknown",
        'speech': 'speech-therapy',
        'sportsmedicine': 'sports-medicine',
        'hematology': 'hematology-oncology',
        'radiologist': 'radiology',
        'obstetrics': 'obstetrics-gynecology',
        'psychiatry-addictive': 'psychiatry-addiction-medicine',
    }

    data['medical_specialty'] = data['medical_specialty'].str.replace('/', '-', regex=False)
    data['medical_specialty'] = data['medical_specialty'].str.replace('&', '-', regex=False)
    data['medical_specialty'] = data['medical_specialty'].str.replace(' ', '-') 

    # Appliquer les corrections
    data['medical_specialty'] = data['medical_specialty'].replace(corrections)

    # Sauvegarder le dataset nettoyé et envoye a minio
    data.to_csv(output_path, index=False)
    print(f"✅ Dataset nettoyé sauvegardé dans {output_path}")

    # upload to minio
    upload_to_minio(str(output_path), "diabetes", "clean/diabetes_cleaned.csv")
    
    logger.info("✅ Cleaned data uploaded to MinIO")