from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
import pandas as pd

# Add parent directory to path so we can import our ETL modules
sys.path.insert(0, '/opt/airflow/etl')

from extract import extract_crypto_data
from transform import transform_crypto_data
from load import load_to_mysql

# Default arguments for the DAG
default_args = {
    'owner': 'data_engineer',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2026, 8, 17),
}

# Define the DAG
dag = DAG(
    'etl_crypto_pipeline',
    default_args=default_args,
    description='Extract crypto prices from CoinGecko, transform, and load to MySQL',
    schedule_interval='@daily',  # Run daily at 00:00 UTC
    catchup=False,
    tags=['etl', 'crypto'],
)

# Define task functions
def extract_task(**context):
    """Extract crypto data from API"""
    print("[EXTRACT] Fetching data from CoinGecko API...")
    raw_data = extract_crypto_data()
    # Push data to next task via XCom
    context['task_instance'].xcom_push(key='raw_data', value=raw_data)
    print(f"[EXTRACT] Successfully fetched {len(raw_data)} coins")
    return True

def transform_task(**context):
    """Transform and clean the data"""
    print("[TRANSFORM] Cleaning data...")
    ti = context['task_instance']
    raw_data = ti.xcom_pull(task_ids='extract_task', key='raw_data')
    
    df = transform_crypto_data(raw_data)
    
    # Convert Timestamp to string for JSON serialization
    df['fetched_at'] = df['fetched_at'].astype(str)
    df_dict = df.to_dict('records')
    ti.xcom_push(key='transformed_df', value=df_dict)
    print(f"[TRANSFORM] Successfully transformed {len(df)} rows")
    return True

def load_task(**context):
    """Load data to MySQL"""
    print("[LOAD] Writing to MySQL...")
    ti = context['task_instance']
    df_dict = ti.xcom_pull(task_ids='transform_task', key='transformed_df')
    
    df = pd.DataFrame(df_dict)
    
    # Use 'mysql' instead of 'localhost' inside Docker
    load_to_mysql(df, host='mysql', port=3306)
    print(f"[LOAD] Successfully loaded data to MySQL")
    return True

# Create tasks
extract = PythonOperator(
    task_id='extract_task',
    python_callable=extract_task,
    provide_context=True,
    dag=dag,
)

transform = PythonOperator(
    task_id='transform_task',
    python_callable=transform_task,
    provide_context=True,
    dag=dag,
)

load = PythonOperator(
    task_id='load_task',
    python_callable=load_task,
    provide_context=True,
    dag=dag,
)

# Set task dependencies: extract >> transform >> load
extract >> transform >> load