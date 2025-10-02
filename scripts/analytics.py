from utils import get_postgresql_engine
from sqlalchemy import text


engine = get_postgresql_engine()

with engine.connect() as conn:
    # Créer le schéma staging s'il n'existe pas
    conn.execute("CREATE SCHEMA IF NOT EXISTS analytics;")
    
    try:
        # --- DimPatient ---
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analytics.dim_patient AS
            SELECT
                ROW_NUMBER() OVER (ORDER BY race, gender, age_num) AS patient_id,
                race,
                gender,
                age_num
            FROM (
                SELECT DISTINCT race, gender, age_num
                FROM staging.diabetes_clean
            ) AS sub;
        """))
        
        # --- DimAdmissionType ---
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analytics.dim_admission_type AS
            SELECT
                ROW_NUMBER() OVER (ORDER BY admission_type) AS admission_type_id,
                admission_type AS admission_type_description
            FROM (
                SELECT DISTINCT admission_type
                FROM staging.diabetes_clean
            ) AS sub;
        """))

        # --- DimDischargeDisposition ---
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analytics.dim_discharge_disposition AS
            SELECT
                ROW_NUMBER() OVER (ORDER BY discharge_disposition) AS discharge_disposition_id,
                discharge_disposition AS discharge_disposition_description
            FROM (
                SELECT DISTINCT discharge_disposition
                FROM staging.diabetes_clean
            ) AS sub;
        """))

        # --- DimAdmissionSource ---
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analytics.dim_admission_source AS
            SELECT
                ROW_NUMBER() OVER (ORDER BY admission_source) AS admission_source_id,
                admission_source AS admission_source_description
            FROM (
                SELECT DISTINCT admission_source
                FROM staging.diabetes_clean
            ) AS sub;
        """))

        # --- DimPayer ---
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analytics.dim_payer AS
            SELECT
                payer_code,
                payer_code AS payer_description
            FROM (
                SELECT DISTINCT payer_code
                FROM staging.diabetes_clean
                WHERE payer_code IS NOT NULL
            ) AS sub;
        """))

        # --- DimMedicalSpecialty ---
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analytics.dim_medical_specialty AS
            SELECT
                ROW_NUMBER() OVER (ORDER BY medical_specialty) AS medical_specialty_id,
                medical_specialty AS medical_specialty_description
            FROM (
                SELECT DISTINCT medical_specialty
                FROM staging.diabetes_clean
                WHERE medical_specialty IS NOT NULL
            ) AS sub;
        """))

        # --- DimDiagnosis ---
        # On fusionne diag_1, diag_2, diag_3 dans une table de diagnostics distincts
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analytics.dim_diagnosis AS
            SELECT
                ROW_NUMBER() OVER (ORDER BY diag_code) AS diag_id,
                diag_code,
                NULL::TEXT AS diag_description
            FROM (
                SELECT DISTINCT diag_1 AS diag_code FROM staging.diabetes_clean WHERE diag_1 IS NOT NULL
                UNION
                SELECT DISTINCT diag_2 AS diag_code FROM staging.diabetes_clean WHERE diag_2 IS NOT NULL
                UNION
                SELECT DISTINCT diag_3 AS diag_code FROM staging.diabetes_clean WHERE diag_3 IS NOT NULL
            ) AS diag_codes;
        """))

        # --- DimTreatment ---
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analytics.dim_treatment AS
            SELECT
                ROW_NUMBER() OVER (ORDER BY metformin, repaglinide, nateglinide, chlorpropamide, glimepiride,
                    acetohexamide, glipizide, glyburide, tolbutamide, pioglitazone,
                    rosiglitazone, acarbose, miglitol, troglitazone, tolazamide, examide,
                    citoglipton, insulin, glyburide_metformin, glipizide_metformin,
                    glimepiride_pioglitazone, metformin_rosiglitazone, metformin_pioglitazone,
                    diabetesMed, change
                ) AS treatment_id,
                metformin, repaglinide, nateglinide, chlorpropamide, glimepiride,
                acetohexamide, glipizide, glyburide, tolbutamide, pioglitazone,
                rosiglitazone, acarbose, miglitol, troglitazone, tolazamide, examide,
                citoglipton, insulin, glyburide_metformin, glipizide_metformin,
                glimepiride_pioglitazone, metformin_rosiglitazone, metformin_pioglitazone,
                diabetesMed, change
            FROM (
                SELECT DISTINCT
                    metformin, repaglinide, nateglinide, chlorpropamide, glimepiride,
                    acetohexamide, glipizide, glyburide, tolbutamide, pioglitazone,
                    rosiglitazone, acarbose, miglitol, troglitazone, tolazamide, examide,
                    citoglipton, insulin, glyburide_metformin, glipizide_metformin,
                    glimepiride_pioglitazone, metformin_rosiglitazone, metformin_pioglitazone,
                    diabetesMed, change
                FROM staging.diabetes_clean
            ) AS sub;
        """))

        # --- FactAdmission ---
        # Jointure avec les dimensions pour récupérer les clés
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analytics.fact_admission AS
            SELECT
                ROW_NUMBER() OVER () AS admission_id,
                p.patient_id,
                a.admission_type_id,
                d.discharge_disposition_id,
                s.admission_source_id,
                pay.payer_code,
                m.medical_specialty_id,
                diag1.diag_id AS diag_1_id,
                diag2.diag_id AS diag_2_id,
                diag3.diag_id AS diag_3_id,
                t.treatment_id,
                f.time_in_hospital,
                f.num_lab_procedures,
                f.num_procedures,
                f.num_medications,
                f.number_outpatient,
                f.number_emergency,
                f.number_inpatient,
                f.number_diagnoses,
                CASE WHEN f.readmitted = '<30' THEN 1
                    WHEN f.readmitted = '>30' THEN 0
                    ELSE NULL END AS readmitted
            FROM staging.diabetes_clean f
            JOIN analytics.dim_patient p
                ON f.race = p.race AND f.gender = p.gender AND f.age_num = p.age_num
            JOIN analytics.dim_admission_type a
                ON f.admission_type = a.admission_type_description
            JOIN analytics.dim_discharge_disposition d
                ON f.discharge_disposition = d.discharge_disposition_description
            JOIN analytics.dim_admission_source s
                ON f.admission_source = s.admission_source_description
            LEFT JOIN analytics.dim_payer pay
                ON f.payer_code = pay.payer_code
            LEFT JOIN analytics.dim_medical_specialty m
                ON f.medical_specialty = m.medical_specialty_description
            LEFT JOIN analytics.dim_diagnosis diag1
                ON f.diag_1 = diag1.diag_code
            LEFT JOIN analytics.dim_diagnosis diag2
                ON f.diag_2 = diag2.diag_code
            LEFT JOIN analytics.dim_diagnosis diag3
                ON f.diag_3 = diag3.diag_code
            JOIN analytics.dim_treatment t
                ON f.metformin = t.metformin
                AND f.repaglinide = t.repaglinide
                AND f.nateglinide = t.nateglinide
                AND f.chlorpropamide = t.chlorpropamide
                AND f.glimepiride = t.glimepiride
                AND f.acetohexamide = t.acetohexamide
                AND f.glipizide = t.glipizide
                AND f.glyburide = t.glyburide
                AND f.tolbutamide = t.tolbutamide
                AND f.pioglitazone = t.pioglitazone
                AND f.rosiglitazone = t.rosiglitazone
                AND f.acarbose = t.acarbose
                AND f.miglitol = t.miglitol
                AND f.troglitazone = t.troglitazone
                AND f.tolazamide = t.tolazamide
                AND f.examide = t.examide
                AND f.citoglipton = t.citoglipton
                AND f.insulin = t.insulin
                AND f.glyburide_metformin = t.glyburide_metformin
                AND f.glipizide_metformin = t.glipizide_metformin
                AND f.glimepiride_pioglitazone = t.glimepiride_pioglitazone
                AND f.metformin_rosiglitazone = t.metformin_rosiglitazone
                AND f.metformin_pioglitazone = t.metformin_pioglitazone
                AND f.diabetesMed = t.diabetesMed
                AND f.change = t.change;
        """))
        print("✅ Data Warehouse créé avec faits et dimensions selon ton modèle !")
    except Exception as e:
        print(f"❌ Erreur lors de la création du Data Warehouse : {e}") 