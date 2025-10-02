CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.dim_diagnosis (
                        diag_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        diag_code TEXT NOT NULL UNIQUE,
                        diag_description TEXT
                    );