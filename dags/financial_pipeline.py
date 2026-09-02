from airflow.sdk import dag, task
from datetime import datetime, timedelta


@dag(
    dag_id="financial_pipeline",
    start_date=datetime(2026, 9, 1),
    schedule=None,
    catchup=False,
)
def financial_pipeline():

    @task(
        retries=3,
        retry_delay=timedelta(minutes=5),
    )
    def extract():
        from src.config.symbols import SYMBOLS
        from src.extract import extract_companies_info
        from src.load import save_raw_data

        data = extract_companies_info(*SYMBOLS)

        if data is None:
            raise ValueError("No company data was extracted")

        save_raw_data(data)

    @task
    def transform():
        import pandas as pd
        from pathlib import Path
        from src.transform import transform_company_data

        data = pd.read_csv("data/raw/company_data.csv")

        clean_data = transform_company_data(data)

        output_path = Path("data/staging/company_data_transformed.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        clean_data.to_csv(output_path, index=False)

    @task
    def validate():
        import pandas as pd
        from src.validate import validate_company_data

        data = pd.read_csv("data/staging/company_data_transformed.csv")

        validate_company_data(data)

    @task
    def load():
        import pandas as pd
        from src.load import save_clean_data, load_to_postgres

        data = pd.read_csv("data/staging/company_data_transformed.csv")

        save_clean_data(data)
        load_to_postgres(data)

    extract() >> transform() >> validate() >> load()


financial_pipeline()