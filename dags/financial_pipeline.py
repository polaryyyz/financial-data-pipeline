from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

def extract_task():
    from src.config.symbols import SYMBOLS
    from src.extract import extract_companies_info
    from src.load import save_raw_data

    data = extract_companies_info(*SYMBOLS)

    if data is None:
        raise ValueError("No company data was extracted")

    save_raw_data(data)

def transform_task():
    from src.transform import transform_company_data
    import pandas as pd
    from pathlib import Path

    data = pd.read_csv("data/raw/company_data.csv")

    clean_data = transform_company_data(data)

    output_path = Path("data/staging/company_data_transformed.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    clean_data.to_csv(output_path, index=False)

def load_task():
    from src.load import save_clean_data
    import pandas as pd

    data = pd.read_csv("data/staging/company_data_transformed.csv")

    save_clean_data(data)

with DAG(
    dag_id="financial_pipeline",
    start_date=datetime(2026, 9, 1),
    schedule=None,
    catchup=False,
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_task,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_task,
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_task,
    )

    extract >> transform >> load