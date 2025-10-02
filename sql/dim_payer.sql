CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.dim_payer (
    payer_code TEXT PRIMARY KEY,
    payer_description TEXT
);