-- Chargement des dimensions avec CTE inline pour les descriptions

-- 1. dim_patient
INSERT INTO analytics.dim_patient (race, gender, age_num)
SELECT DISTINCT race, gender, age_num
FROM staging.diabetes_clean
WHERE race IS NOT NULL AND gender IS NOT NULL AND age_num IS NOT NULL
  AND (race, gender, age_num) NOT IN (
    SELECT race, gender, age_num FROM analytics.dim_patient
);

-- 2. dim_admission_type
WITH admission_type_map (admission_type_id, admission_type_description) AS (
  VALUES
    (1, 'Emergency'),
    (2, 'Urgent'),
    (3, 'Elective'),
    (4, 'Newborn'),
    (5, 'Trauma Center'),
    (6, 'Not Available'),
    (7, 'Other'),
    (8, 'Unknown') 
)
INSERT INTO analytics.dim_admission_type (admission_type_id, admission_type_description)
SELECT DISTINCT m.admission_type_id, m.admission_type_description
FROM staging.diabetes_clean d
JOIN admission_type_map m ON d.admission_type_id = m.admission_type_id
WHERE m.admission_type_description NOT IN (
    SELECT admission_type_description FROM analytics.dim_admission_type
);


-- 3. dim_discharge_disposition
WITH discharge_disposition_map (discharge_disposition_id, discharge_disposition_description) AS (
  VALUES
    (1,  'Discharged to home'),
    (2,  'Discharged/transferred to another short term hospital'),
    (3,  'Discharged/transferred to SNF'),  -- Skilled Nursing Facility
    (4,  'Discharged/transferred to ICF'),  -- Intermediate Care Facility
    (5,  'Discharged/transferred to another type of institution'),
    (6,  'Discharged/transferred to home with home health service'),
    (7,  'Left AMA'),  -- Against Medical Advice
    (8,  'Expired'),
    (9,  'Discharged/transferred to hospital-based hospice'),
    (10, 'Discharged/transferred to Medicare certified long term care hospital'),
    (11, 'Not Mapped'),
    (12, 'Still patient'),
    (13, 'Discharged/transferred to Federal health care facility'),
    (14, 'Discharged/transferred to cancer center or children’s hospital'),
    (15, 'Discharged/transferred to critical access hospital'),
    (16, 'Discharged/transferred to psychiatric hospital'),
    (17, 'Discharged/transferred to rehab facility'),
    (18, 'Discharged/transferred to long term care hospital'),
    (19, 'Discharged/transferred to swing bed'),
    (20, 'Discharged/transferred to court/law enforcement'),
    (21, 'Discharged/transferred to non-healthcare facility'),
    (22, 'Hospice - home'),
    (23, 'Hospice - medical facility'),
    (24, 'Expired at home. Medicaid only, hospice.'),
    (25, 'Expired in a medical facility. Medicaid only, hospice.'),
    (26, 'Unknown/Not Reported'),          -- placeholder à ajuster
    (27, 'Discharged/transferred to other facility'),  -- placeholder à ajuster
    (28, 'Discharged/transferred to another type of care')  -- placeholder à ajuster
)
INSERT INTO analytics.dim_discharge_disposition (discharge_disposition_id, discharge_disposition_description)
SELECT DISTINCT m.discharge_disposition_id, m.discharge_disposition_description
FROM staging.diabetes_clean d
JOIN discharge_disposition_map m ON d.discharge_disposition_id = m.discharge_disposition_id
WHERE m.discharge_disposition_description NOT IN (
    SELECT discharge_disposition_description FROM analytics.dim_discharge_disposition
);



-- 4. dim_admission_source
WITH admission_source_map (admission_source_id, admission_source_description) AS (
  VALUES
    (1,  'Physician Referral'),
    (2,  'Clinic Referral'),
    (3,  'HMO Referral'),
    (4,  'Transfer from a hospital'),
    (5,  'Transfer from a Skilled Nursing Facility (SNF)'),
    (6,  'Transfer from another health care facility'),
    (7,  'Emergency Room'),
    (8,  'Court/Law Enforcement'),
    (9,  'Transfer from Hospice'),
    (10, 'Transfer from Long Term Care Hospital'),
    (11, 'Transfer from Psychiatric Hospital'),
    (12, 'Transfer from Rehabilitation Facility'),
    (13, 'Transfer from Federal Health Care Facility'),
    (14, 'Transfer from VA Facility'),
    (15, 'Transfer from a Cancer Center'),
    (16, 'Transfer from a Children’s Hospital'),
    (17, 'Transfer from Critical Access Hospital'),
    (18, 'Transfer from Home Health Care'),
    (19, 'Transfer from Outpatient Facility'),
    (20, 'Other'),
    (21, 'Information Not Available'),
    (22, 'Transfer from Unknown Facility'),
    (23, 'Transfer from Community Hospital'),
    (24, 'Transfer from Mobile Care Unit'),
    (25, 'Transfer from Telemedicine Service')
)
INSERT INTO analytics.dim_admission_source (admission_source_id, admission_source_description)
SELECT DISTINCT m.admission_source_id, m.admission_source_description
FROM staging.diabetes_clean d
JOIN admission_source_map m ON d.admission_source_id = m.admission_source_id
WHERE m.admission_source_description NOT IN (
    SELECT admission_source_description FROM analytics.dim_admission_source
);


-- 5. dim_payer
INSERT INTO analytics.dim_payer (payer_code)
SELECT DISTINCT payer_code
FROM staging.diabetes_clean
WHERE payer_code IS NOT NULL
  AND payer_code NOT IN (
    SELECT payer_code FROM analytics.dim_payer
);

-- 6. dim_medical_specialty
INSERT INTO analytics.dim_medical_specialty (medical_specialty_description)
SELECT DISTINCT medical_specialty
FROM staging.diabetes_clean
WHERE medical_specialty IS NOT NULL
  AND medical_specialty NOT IN (
    SELECT medical_specialty_description FROM analytics.dim_medical_specialty
);

-- 7. dim_diagnosis
INSERT INTO analytics.dim_diagnosis (diag_code)
SELECT DISTINCT diag
FROM (
    SELECT diag_1 AS diag FROM staging.diabetes_clean
    UNION
    SELECT diag_2 FROM staging.diabetes_clean
    UNION
    SELECT diag_3 FROM staging.diabetes_clean
) AS all_diags
WHERE diag IS NOT NULL
  AND diag NOT IN (
    SELECT diag_code FROM analytics.dim_diagnosis
);

-- 8. dim_treatment
INSERT INTO analytics.dim_treatment (
    metformin, repaglinide, nateglinide, chlorpropamide,
    glimepiride, acetohexamide, glipizide, glyburide,
    tolbutamide, pioglitazone, rosiglitazone, acarbose,
    miglitol, troglitazone, tolazamide, examide,
    citoglipton, insulin, glyburide_metformin,
    glipizide_metformin, glimepiride_pioglitazone,
    metformin_rosiglitazone, metformin_pioglitazone,
    diabetesMed, change
)
SELECT DISTINCT
    metformin, repaglinide, nateglinide, chlorpropamide,
    glimepiride, acetohexamide, glipizide, glyburide,
    tolbutamide, pioglitazone, rosiglitazone, acarbose,
    miglitol, troglitazone, tolazamide, examide,
    citoglipton, insulin, glyburide_metformin,
    glipizide_metformin, glimepiride_pioglitazone,
    metformin_rosiglitazone, metformin_pioglitazone,
    diabetesMed, change
FROM staging.diabetes_clean
EXCEPT
SELECT
    metformin, repaglinide, nateglinide, chlorpropamide,
    glimepiride, acetohexamide, glipizide, glyburide,
    tolbutamide, pioglitazone, rosiglitazone, acarbose,
    miglitol, troglitazone, tolazamide, examide,
    citoglipton, insulin, glyburide_metformin,
    glipizide_metformin, glimepiride_pioglitazone,
    metformin_rosiglitazone, metformin_pioglitazone,
    diabetesMed, change
FROM analytics.dim_treatment;
