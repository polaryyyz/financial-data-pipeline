import os
import pandas as pd
from sqlalchemy import create_engine, text, URL
from src.load import (
    load_to_postgres,
    load_company_snapshots,
)

def get_engine():
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("WAREHOUSE_USER"),
        password=os.getenv("WAREHOUSE_PASSWORD"),
        host=os.getenv("WAREHOUSE_HOST"),
        port=int(os.getenv("WAREHOUSE_PORT")),
        database=os.getenv("WAREHOUSE_DB"),
    )

    return create_engine(url)


def sample_company_data():
    return pd.DataFrame(
        {
            "symbol": ["AAPL", "MSFT"],
            "companyName": ["Apple Inc.", "Microsoft Corporation"],
            "price": [230.0, 420.0],
            "marketCap": [
                3_000_000_000_000,
                2_500_000_000_000,
            ],
            "sector": ["Technology", "Technology"],
            "industry": ["Consumer Electronics", "Software"],
            "country": ["US", "US"],
            "exchange": ["NASDAQ", "NASDAQ"],
            "marketCap_billions": [3000.0, 2500.0],
        }
    )

def test_load_to_postgres_upsert():
    data = sample_company_data()

    load_to_postgres(data)

    updated_data = data.copy()
    updated_data.loc[
        updated_data["symbol"] == "AAPL",
        "price",
    ] = 250.0

    load_to_postgres(updated_data)

    engine = get_engine()

    with engine.connect() as connection:
        count = connection.execute(
            text("SELECT COUNT(*) FROM companies")
        ).scalar()

        apple_price = connection.execute(
            text(
                """
                SELECT price
                FROM companies
                WHERE symbol = 'AAPL'
                """
            )
        ).scalar()

    assert count == 2
    assert apple_price == 250.0

def test_company_snapshots_are_idempotent():
    data = sample_company_data()

    load_company_snapshots(
        data,
        "integration_run_001",
    )

    load_company_snapshots(
        data,
        "integration_run_001",
    )

    engine = get_engine()

    with engine.connect() as connection:
        count = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM company_snapshots
                WHERE pipeline_run_id = 'integration_run_001'
                """
            )
        ).scalar()

    assert count == 2

def test_company_snapshots_keep_history():
    data = sample_company_data()

    load_company_snapshots(
        data,
        "integration_run_002",
    )

    load_company_snapshots(
        data,
        "integration_run_003",
    )

    engine = get_engine()

    with engine.connect() as connection:
        count = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM company_snapshots
                WHERE pipeline_run_id IN (
                    'integration_run_002',
                    'integration_run_003'
                )
                """
            )
        ).scalar()

    assert count == 4