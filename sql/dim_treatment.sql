CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.dim_treatment (
                        treatment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        metformin TEXT, repaglinide TEXT, nateglinide TEXT, chlorpropamide TEXT, glimepiride TEXT,
                        acetohexamide TEXT, glipizide TEXT, glyburide TEXT, tolbutamide TEXT, pioglitazone TEXT,
                        rosiglitazone TEXT, acarbose TEXT, miglitol TEXT, troglitazone TEXT, tolazamide TEXT, examide TEXT,
                        citoglipton TEXT, insulin TEXT, glyburide_metformin TEXT, glipizide_metformin TEXT,
                        glimepiride_pioglitazone TEXT, metformin_rosiglitazone TEXT, metformin_pioglitazone TEXT,
                        diabetesMed TEXT, change TEXT
                    );