-- ==========================================================
-- Remplissage de la table de faits : analytics.fact_admission
-- Source : staging.diabetes_clean + tables de dimensions
-- ==========================================================

INSERT INTO analytics.fact_admission (
    admission_id,
    patient_id,
    admission_type_id,
    discharge_disposition_id,
    admission_source_id,
    payer_code,
    medical_specialty_id,
    diag_1_id,
    diag_2_id,
    diag_3_id,
    treatment_id,
    time_in_hospital,
    num_lab_procedures,
    num_procedures,
    num_medications,
    number_outpatient,
    number_emergency,
    number_inpatient,
    number_diagnoses,
    readmitted
)
SELECT
    ROW_NUMBER() OVER () AS admission_id,
    p.patient_id,
    f.admission_type_id,
    f.discharge_disposition_id,
    f.admission_source_id,
    f.payer_code,
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
    CASE 
        WHEN f.readmitted = '<30' THEN TRUE
        WHEN f.readmitted = '>30' THEN FALSE
        ELSE NULL 
    END AS readmitted
FROM staging.diabetes_clean f
JOIN analytics.dim_patient p
    ON f.race = p.race 
    AND f.gender = p.gender 
    AND f.age_num = p.age_num
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