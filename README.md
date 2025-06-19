# E-commerce Data Pipeline with Airflow

## 📦 Description

Ce projet met en place un pipeline de traitement automatisé de données e-commerce à l’aide d’Airflow.

Les données proviennent du fichier **"Online Retail II"** publié sur le [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II). Elles contiennent des transactions B2C effectuées par un distributeur britannique entre 2010 et 2011, incluant des colonnes telles que :
- InvoiceNo
- StockCode
- Description
- Quantity
- Price (remplacé ici par UnitPrice)
- CustomerID
- Country

## ⚙️ Architecture Docker

Le projet repose sur une stack Docker avec les services suivants :
- `airflow`: Webserver Airflow (port 8090)
- `airflow_scheduler`: Scheduler dédié
- `mysql`: Base de données (port exposé : 3307)
- `phpmyadmin`: Interface de gestion MySQL (port exposé : 8081)
- `redis`: Service de cache utilisé par Airflow

## 📂 Pipeline Airflow

1. **Conversion des données** : le fichier Excel est converti en CSV via `data/download.py`
2. **Chargement dans MySQL** : les données nettoyées (gestion des NaN via `safe_val`) sont insérées dans la base `data_airflow`, table `sales` via un DAG Airflow quotidien planifié à 6h.
3. **Connexion sécurisée** : l’accès à MySQL est configuré dynamiquement à l’aide d’un hook Airflow (`BaseHook.get_connection('mysql_conn')`), pour éviter de stocker les identifiants en dur.

## 🐍 Exemple de script Python

Fichier : `dags/ecommerce_data_pipeline.py`

- Lit le fichier `/opt/airflow/data/online_retail.csv`
- Nettoie chaque ligne (gestion des valeurs manquantes)
- Insère les données dans MySQL via un `PythonOperator`

## 📦 docker-compose.yml

Le fichier `docker-compose.yml` définit la configuration complète, notamment :
- Le montage des volumes (`dags`, `data`, `logs`, `config`)
- L'installation des dépendances via `requirements.txt`
- Le démarrage conditionnel basé sur la disponibilité de MySQL

## ▶️ Lancement

1. Cloner ce dépôt
2. Convertir le fichier Excel : `python data/download.py`
3. Lancer la stack : `docker-compose up -d`
4. Accéder à l'interface Airflow sur [http://localhost:8090](http://localhost:8090)
5. Lancer manuellement le DAG `ecommerce_data_pipeline`

## 🛠 Requis
- Docker & Docker Compose
- Le fichier source Excel `online_retail_II.xlsx`

## 🧾 License

Ce projet est un projet d’apprentissage basé sur un dataset public.