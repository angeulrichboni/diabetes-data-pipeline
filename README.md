# Projet Data Pipeline Diabète

## Objectif
Ce projet met en place un pipeline de données complet pour l'analyse des hospitalisations liées au diabète, basé sur le jeu de données UCI "Diabetes 130-US hospitals for years 1999-2008". Il permet d'extraire, transformer, stocker et modéliser les données dans un Data Warehouse (PostgreSQL), orchestré par Airflow et stocké sur MinIO.

## Architecture
- **Airflow** : Orchestration des tâches ETL (extraction, transformation, chargement, modélisation).
- **MinIO** : Stockage objet des fichiers bruts et nettoyés.
- **PostgreSQL** : Base de données relationnelle pour staging et Data Warehouse (schémas `staging` et `analytics`).
- **Docker Compose** : Déploiement de l'ensemble des services (Airflow, MinIO, PostgreSQL, Redis).

## Pipeline ETL
1. **Extraction** :
   - Téléchargement du dataset depuis l'UCI Repository.
   - Stockage du fichier brut sur MinIO.
2. **Transformation** :
   - Nettoyage des données (suppression/complétion des valeurs manquantes, normalisation, création de variables).
   - Stockage du fichier nettoyé sur MinIO.
3. **Staging** :
   - Chargement des données nettoyées dans la table `staging.diabetes_clean` (PostgreSQL).
4. **Modélisation** :
   - Création et alimentation des dimensions et de la table de faits dans le schéma `analytics` (Data Warehouse).

## Démarrage rapide
### Prérequis
- Docker et Docker Compose
- (Optionnel) Python 3.11+ pour exécuter les scripts localement

### Lancement du projet
1. Copier le fichier `.env.example` en `.env` et renseigner les variables nécessaires (identifiants MinIO, PostgreSQL, Airflow).
2. Lancer la stack :
   ```bash
   docker-compose up --build
   ```
3. Accéder à l'interface Airflow : [http://localhost:5005](http://localhost:5005)
4. Déclencher le DAG `diabetes_dag` pour exécuter le pipeline complet.

## Structure des dossiers
- `airflow/dags/` : DAG Airflow et scripts ETL Python
- `airflow/dags/sql/` : Scripts SQL pour la modélisation du Data Warehouse
- `scripts/` : Utilitaires pour extraction, transformation, staging, analytics
- `data/` : Données brutes et nettoyées (stockées aussi sur MinIO)
- `sql/` : Scripts de création des tables (staging, dimensions, faits)
- `migrations/` : Scripts Alembic pour la gestion des migrations SQL
- `tests/` : Tests unitaires des utilitaires Python

## Principaux fichiers
- `docker-compose.yml` : Définition des services
- `requirements.txt` : Dépendances Python
- `airflow/dags/dw_pipeline.py` : Définition du pipeline Airflow
- `airflow/dags/utils/` : Fonctions d'extraction, transformation, chargement
- `sql/` : Scripts SQL pour la structure du Data Warehouse

## Tests
Lancer les tests unitaires :
```bash
pytest
```

## Migrations Alembic (PostgreSQL)
Alembic est utilisé pour créer et versionner les tables dans PostgreSQL (schémas `staging` et `analytics`). Les migrations se trouvent dans `migrations/` et sont configurées via `alembic.ini` et `migrations/env.py`.

(Optionnel) Activer l’environnement virtuel si présent :
```bash
source diabete_env/bin/activate
```

4) Appliquer toutes les migrations :
```bash
alembic upgrade head
```

Après exécution, les tables `staging.diabetes_clean`, les dimensions `analytics.dim_*` et la table de faits `analytics.fact_admission` seront créées.

## Auteurs
- Ange BONI

## Remarques
- Le pipeline est conçu pour être facilement extensible à d'autres sources ou modèles analytiques.
- Les identifiants sensibles doivent être gérés via des variables d'environnement.

---

**Ce projet fournit une base robuste pour l'analyse avancée des données hospitalières liées au diabète, de l'extraction à la modélisation analytique.**
