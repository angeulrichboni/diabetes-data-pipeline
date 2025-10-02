CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.fact_admission (
    admission_id              SERIAL PRIMARY KEY,
    patient_id                INTEGER NOT NULL,
    admission_type_id         INTEGER NOT NULL,
    discharge_disposition_id  INTEGER NOT NULL,
    admission_source_id       INTEGER NOT NULL,
    payer_code                VARCHAR(10),
    medical_specialty_id      INTEGER,
    diag_1_id                 INTEGER,
    diag_2_id                 INTEGER,
    diag_3_id                 INTEGER,
    treatment_id              INTEGER NOT NULL,
    time_in_hospital          INTEGER,
    num_lab_procedures        INTEGER,
    num_procedures            INTEGER,
    num_medications           INTEGER,
    number_outpatient         INTEGER,
    number_emergency          INTEGER,
    number_inpatient          INTEGER,
    number_diagnoses          INTEGER,
    readmitted                BOOLEAN,
    
    -- 🔗 Foreign Keys
    CONSTRAINT fk_patient
        FOREIGN KEY (patient_id)
        REFERENCES analytics.dim_patient (patient_id),

    CONSTRAINT fk_admission_type
        FOREIGN KEY (admission_type_id)
        REFERENCES analytics.dim_admission_type (admission_type_id),

    CONSTRAINT fk_discharge_disposition
        FOREIGN KEY (discharge_disposition_id)
        REFERENCES analytics.dim_discharge_disposition (discharge_disposition_id),

    CONSTRAINT fk_admission_source
        FOREIGN KEY (admission_source_id)
        REFERENCES analytics.dim_admission_source (admission_source_id),

    CONSTRAINT fk_payer
        FOREIGN KEY (payer_code)
        REFERENCES analytics.dim_payer (payer_code),

    CONSTRAINT fk_medical_specialty
        FOREIGN KEY (medical_specialty_id)
        REFERENCES analytics.dim_medical_specialty (medical_specialty_id),

    CONSTRAINT fk_diag_1
        FOREIGN KEY (diag_1_id)
        REFERENCES analytics.dim_diagnosis (diag_id),

    CONSTRAINT fk_diag_2
        FOREIGN KEY (diag_2_id)
        REFERENCES analytics.dim_diagnosis (diag_id),

    CONSTRAINT fk_diag_3
        FOREIGN KEY (diag_3_id)
        REFERENCES analytics.dim_diagnosis (diag_id),

    CONSTRAINT fk_treatment
        FOREIGN KEY (treatment_id)
        REFERENCES analytics.dim_treatment (treatment_id)
);
