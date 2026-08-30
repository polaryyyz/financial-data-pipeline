from pathlib import Path
from unittest.mock import patch, MagicMock, call
from src.load import save_raw_data
from src.load import save_clean_data
import pandas as pd

def test_save_raw_data_success(tmp_path):
    with patch("src.load.Path") as Mock_Path:
        mock_output_path = tmp_path/"data/raw/company_data.csv"
        Mock_Path.return_value = mock_output_path
        data = pd.DataFrame({
        "symbol": ["AAPL", "MSFT", "NVDA"],
        "companyName": ["Apple Inc.", "Microsoft Corporation", "NVIDIA Corporation"],
        "price": [310.34, 487.31, 208.48],
        "marketCap": [4558074061040, 3618544770500, 5049594080000],
        "sector": ["Technology", "Technology", "Technology"],
        "industry": [
            "Consumer Electronics",
            "Software - Infrastructure",
            "Semiconductors"
        ],
        "country": ["US", "US", "US"],
        "exchange": ["NASDAQ", "NASDAQ", "NASDAQ"]            
        })

        save_raw_data(data)

        assert mock_output_path.exists()
        assert data.equals(pd.read_csv(mock_output_path))

def test_save_raw_data_success_oserror(tmp_path):
    with patch("src.load.Path") as Mock_Path:
        mock_output_path = tmp_path/"data/raw/company_data.csv"
        Mock_Path.return_value = mock_output_path
        data = pd.DataFrame({
        "symbol": ["AAPL", "MSFT", "NVDA"],
        "companyName": ["Apple Inc.", "Microsoft Corporation", "NVIDIA Corporation"],
        "price": [310.34, 487.31, 208.48],
        "marketCap": [4558074061040, 3618544770500, 5049594080000],
        "sector": ["Technology", "Technology", "Technology"],
        "industry": [
            "Consumer Electronics",
            "Software - Infrastructure",
            "Semiconductors"
        ],
        "country": ["US", "US", "US"],
        "exchange": ["NASDAQ", "NASDAQ", "NASDAQ"]            
        })

        data.to_csv = MagicMock(side_effect = OSError)
 
        save_raw_data(data)

        data.to_csv.assert_called_once_with(mock_output_path, index=False)

def test_save_clean_data(tmp_path):
    with patch("src.load.Path") as Mock_Path:
        mock_output_path = tmp_path/"data/processed/company_data.csv"
        Mock_Path.return_value = mock_output_path
        data = pd.DataFrame({
        "symbol": ["AAPL", "MSFT", "NVDA"],
        "companyName": ["Apple Inc.", "Microsoft Corporation", "NVIDIA Corporation"],
        "price": [310.34, 487.31, 208.48],
        "marketCap": [4558074061040, 3618544770500, 5049594080000],
        "sector": ["Technology", "Technology", "Technology"],
        "industry": [
            "Consumer Electronics",
            "Software - Infrastructure",
            "Semiconductors"
        ],
        "country": ["US", "US", "US"],
        "exchange": ["NASDAQ", "NASDAQ", "NASDAQ"]            
        })

        save_clean_data(data)

        assert mock_output_path.exists()
        assert data.equals(pd.read_csv(mock_output_path))

def test_save_clean_data_oserror(tmp_path):
    with patch("src.load.Path") as Mock_Path:
        mock_output_path = tmp_path/"data/processed/company_data.csv"
        Mock_Path.return_value = mock_output_path
        data = pd.DataFrame({
        "symbol": ["AAPL", "MSFT", "NVDA"],
        "companyName": ["Apple Inc.", "Microsoft Corporation", "NVIDIA Corporation"],
        "price": [310.34, 487.31, 208.48],
        "marketCap": [4558074061040, 3618544770500, 5049594080000],
        "sector": ["Technology", "Technology", "Technology"],
        "industry": [
            "Consumer Electronics",
            "Software - Infrastructure",
            "Semiconductors"
        ],
        "country": ["US", "US", "US"],
        "exchange": ["NASDAQ", "NASDAQ", "NASDAQ"]            
        })

        data.to_csv = MagicMock(side_effect = OSError)

        save_clean_data(data)

        data.to_csv.assert_called_once_with(mock_output_path, index = False)