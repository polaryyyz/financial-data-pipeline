from unittest.mock import patch, MagicMock
from sqlalchemy.dialects import postgresql
import pytest
import pandas as pd
from src.load import (
    load_to_postgres,
    load_company_snapshots,
    save_raw_data,
    save_clean_data,
)

def sample_company_data():
    return pd.DataFrame(
        {
            "symbol": ["AAPL", "MSFT", "NVDA"],
            "companyName": [
                "Apple Inc.",
                "Microsoft Corporation",
                "NVIDIA Corporation",
            ],
            "price": [310.34, 487.31, 208.48],
            "marketCap": [
                4558074061040,
                3618544770500,
                5049594080000,
            ],
            "sector": [
                "Technology",
                "Technology",
                "Technology",
            ],
            "industry": [
                "Consumer Electronics",
                "Software - Infrastructure",
                "Semiconductors",
            ],
            "country": ["US", "US", "US"],
            "exchange": ["NASDAQ", "NASDAQ", "NASDAQ"],
            "marketCap_billions": [
                4558.07,
                3618.54,
                5049.59,
            ],
        }
    )

def test_save_raw_data_success(tmp_path):
    with patch("src.load.Path") as Mock_Path:
        mock_output_path = tmp_path/"data/raw/company_data.csv"
        Mock_Path.return_value = mock_output_path
        data = sample_company_data()

        save_raw_data(data)

        assert mock_output_path.exists()
        assert data.equals(pd.read_csv(mock_output_path))

def test_save_raw_data_success_oserror(tmp_path):
    with patch("src.load.Path") as Mock_Path:
        mock_output_path = tmp_path/"data/raw/company_data.csv"
        Mock_Path.return_value = mock_output_path
        data = sample_company_data()
 
        data.to_csv = MagicMock(side_effect = OSError("Unable to write file"))

        with pytest.raises(OSError):
            save_clean_data(data)

def test_save_clean_data(tmp_path):
    with patch("src.load.Path") as Mock_Path:
        mock_output_path = tmp_path/"data/processed/company_data.csv"
        Mock_Path.return_value = mock_output_path
        data = sample_company_data()

        save_clean_data(data)

        assert mock_output_path.exists()
        assert data.equals(pd.read_csv(mock_output_path))

def test_save_clean_data_oserror(tmp_path):
    with patch("src.load.Path") as Mock_Path:
        mock_output_path = tmp_path/"data/processed/company_data.csv"
        Mock_Path.return_value = mock_output_path
        data = sample_company_data()

        data.to_csv = MagicMock(side_effect = OSError("Unable to write file"))

        with pytest.raises(OSError):
            save_clean_data(data)

def test_load_to_postgres():
    data = sample_company_data()

    env_vars = {
        "WAREHOUSE_USER": "test_user",
        "WAREHOUSE_PASSWORD": "test_password",
        "WAREHOUSE_HOST": "warehouse",
        "WAREHOUSE_PORT": "5432",
        "WAREHOUSE_DB": "test_db",
    }

    with patch.dict("os.environ", env_vars):
        with patch("src.load.create_engine") as mock_create_engine:
            mock_engine = MagicMock()
            mock_connection = MagicMock()

            mock_create_engine.return_value = mock_engine

            mock_engine.begin.return_value.__enter__.return_value = (mock_connection)

            load_to_postgres(data)

            mock_create_engine.assert_called_once()
            mock_engine.begin.assert_called_once()
            mock_connection.execute.assert_called_once()

            statement = mock_connection.execute.call_args.args[0]

            sql = str(statement.compile(dialect=postgresql.dialect()))

            assert "ON CONFLICT (symbol) DO UPDATE" in sql

def test_load_company_snapshots():
    data = sample_company_data()

    env_vars = {
        "WAREHOUSE_USER": "test_user",
        "WAREHOUSE_PASSWORD": "test_password",
        "WAREHOUSE_HOST": "warehouse",
        "WAREHOUSE_PORT": "5432",
        "WAREHOUSE_DB": "test_db",
    }

    with patch.dict("os.environ", env_vars):
        with patch("src.load.create_engine") as mock_create_engine:
            mock_engine = MagicMock()
            mock_connection = MagicMock()

            mock_create_engine.return_value = mock_engine

            mock_engine.begin.return_value.__enter__.return_value = (mock_connection)

            load_company_snapshots(
                data,
                "test_run_001",
            )

            mock_create_engine.assert_called_once()
            mock_engine.begin.assert_called_once()
            mock_connection.execute.assert_called_once()

            statement = mock_connection.execute.call_args.args[0]

            sql = str(statement.compile(dialect=postgresql.dialect()))

            assert (
                "ON CONFLICT (symbol, pipeline_run_id) "
                "DO NOTHING"
                in sql
            )