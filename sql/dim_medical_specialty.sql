CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.dim_medical_specialty (
                        medical_specialty_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        medical_specialty_description TEXT NOT NULL UNIQUE
                    );