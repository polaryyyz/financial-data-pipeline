import os
import logging
from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Float,
    BigInteger,
    DateTime,
    URL,
)
from sqlalchemy.dialects.postgresql import insert

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
    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("WAREHOUSE_USER"),
        password=os.getenv("WAREHOUSE_PASSWORD"),
        host=os.getenv("WAREHOUSE_HOST"),
        port=int(os.getenv("WAREHOUSE_PORT")),
        database=os.getenv("WAREHOUSE_DB"),
    )

    engine = create_engine(connection_url)

    metadata = MetaData()

    companies = Table(
        "companies",
        metadata,
        Column("symbol", String, primary_key=True),
        Column("companyName", String),
        Column("price", Float),
        Column("marketCap", BigInteger),
        Column("sector", String),
        Column("industry", String),
        Column("country", String),
        Column("exchange", String),
        Column("marketCap_billions", Float),
    )

    metadata.create_all(engine)

    records = dataframe.to_dict(orient="records")

    insert_statement = insert(companies).values(records)

    update_columns = {
        column.name: insert_statement.excluded[column.name]
        for column in companies.columns
        if column.name != "symbol"
    }

    upsert_statement = insert_statement.on_conflict_do_update(
        index_elements=["symbol"],
        set_=update_columns,
    )

    with engine.begin() as connection:
        connection.execute(upsert_statement)

    logger.info("Company data upserted successfully into PostgreSQL")

def load_company_snapshots(dataframe, pipeline_run_id):
    dataframe = dataframe.copy()

    dataframe["snapshot_at"] = datetime.now(timezone.utc)
    dataframe["pipeline_run_id"] = pipeline_run_id

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("WAREHOUSE_USER"),
        password=os.getenv("WAREHOUSE_PASSWORD"),
        host=os.getenv("WAREHOUSE_HOST"),
        port=int(os.getenv("WAREHOUSE_PORT")),
        database=os.getenv("WAREHOUSE_DB"),
    )

    engine = create_engine(connection_url)
    metadata = MetaData()

    company_snapshots = Table(
        "company_snapshots",
        metadata,
        Column("symbol", String, primary_key=True),
        Column("pipeline_run_id", String, primary_key=True),
        Column("companyName", String),
        Column("price", Float),
        Column("marketCap", BigInteger),
        Column("sector", String),
        Column("industry", String),
        Column("country", String),
        Column("exchange", String),
        Column("marketCap_billions", Float),
        Column("snapshot_at", DateTime(timezone=True)),
    )

    metadata.create_all(engine)

    records = dataframe.to_dict(orient="records")

    insert_statement = insert(company_snapshots).values(records)

    insert_statement = insert_statement.on_conflict_do_nothing(
        index_elements=["symbol", "pipeline_run_id"]
    )

    with engine.begin() as connection:
        connection.execute(insert_statement)

    logger.info(
        "Company snapshot data loaded successfully into PostgreSQL"
    )