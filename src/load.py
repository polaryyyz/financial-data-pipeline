import os
import logging
from pathlib import Path
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

def save_raw_data(dataframe):
    try: 
        output_path = Path("data/raw/company_data.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        dataframe.to_csv(output_path, index=False)
        logger.info(f"File creation completed: {output_path}")

    except OSError as os_err:
        logger.error(f"Error with input/output: {os_err}")

def save_clean_data(dataframe):
    try: 
        output_path = Path("data/processed/company_data_clean.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        dataframe.to_csv(output_path, index=False)
        logger.info(f"Clean file creation completed: {output_path}")

    except OSError as os_err:
        logger.error(f"Error with input/output: {os_err}")
        raise

def load_to_postgres(dataframe):
    user = os.getenv("WAREHOUSE_USER")
    password = os.getenv("WAREHOUSE_PASSWORD")
    host = os.getenv("WAREHOUSE_HOST")
    port = os.getenv("WAREHOUSE_PORT")
    database = os.getenv("WAREHOUSE_DB")

    connection_url = (
        f"postgresql+psycopg2://{user}:{password}"
        f"@{host}:{port}/{database}"
    )

    engine = create_engine(connection_url)

    dataframe.to_sql(
        "companies",
        engine,
        if_exists="replace",
        index=False,
    )

    logger.info("Company data loaded successfully into PostgreSQL")