from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
import mysql.connector
import pandas as pd
import math
from datetime import datetime

def safe_val(val):
    """
    Retourne None si la valeur est un float NaN, sinon renvoie la valeur.
    """
    if isinstance(val, float) and math.isnan(val):
        return None
    return val

def load_data_to_mysql():
    # Charger le fichier CSV avec pandas
    df = pd.read_csv('/opt/airflow/data/online_retail.csv')
    
    # Récupérer les informations de connexion via Airflow
    conn_details = BaseHook.get_connection('mysql_conn')
    host = conn_details.host
    user = conn_details.login
    password = conn_details.password
    database = conn_details.schema  # Le schéma correspond à la base de données à utiliser

    # Établir la connexion MySQL
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()

    # Parcourir chaque ligne du DataFrame pour insérer les données dans la table 'sales'
    for _, row in df.iterrows():
        # Pour chaque colonne, appliquer la conversion safe_val
        invoice_no   = safe_val(row['InvoiceNo'])
        stock_code   = safe_val(row['StockCode'])
        description  = safe_val(row['Description'])
        quantity     = safe_val(row['Quantity'])
        invoice_date = safe_val(row['InvoiceDate'])
        unit_price   = safe_val(row['Price'])         # On suppose que 'Price' correspond à 'UnitPrice'
        customer_id  = safe_val(row['CustomerID'])      # Vérifier l'orthographe par rapport au CSV
        country      = safe_val(row['Country'])

        # Exécuter la requête d'insertion en passant None pour les valeurs manquantes
        cursor.execute("""
            INSERT INTO sales (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            invoice_no,
            stock_code,
            description,
            quantity,
            invoice_date,
            unit_price,
            customer_id,
            country
        ))
    
    # Valider les modifications et fermer la connexion
    conn.commit()
    cursor.close()
    conn.close()

# Définir les paramètres du DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 30),
    'retries': 0,  # Aucun réessai en cas d'échec
}

# Définition du DAG
with DAG('ecommerce_data_pipeline', 
         default_args=default_args, 
         schedule_interval=None,
         catchup=False) as dag:

    # Définition de la tâche qui charge les données dans MySQL
    load_data_task = PythonOperator(
        task_id='load_data_to_mysql',
        python_callable=load_data_to_mysql,
        dag=dag 
    )

    load_data_task