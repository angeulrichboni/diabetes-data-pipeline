CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.dim_patient (
    patient_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    race TEXT NOT NULL,
    gender TEXT NOT NULL,
    age_num INT NOT NULL,
    CONSTRAINT uq_dim_patient UNIQUE (race, gender, age_num)
);