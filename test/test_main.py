from unittest.mock import patch
from src.main import main
from src.config import logging_config
from src.config.symbols import SYMBOLS
import pandas as pd

def test_main():
    with patch("src.main.extract_companies_info") as mock_extract:
        data = pd.DataFrame(
            {
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
            }
        )

        mock_extract.return_value = data

        with patch("src.main.save_raw_data") as mock_save_raw:
            with patch("src.main.transform_company_data") as mock_transform:
                clean_data = pd.DataFrame(
                    {
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
                    }
                )
                
                mock_transform.return_value = clean_data

                with patch("src.main.save_clean_data") as mock_save_clean:
                    main()
                    mock_extract.assert_called_once_with(*SYMBOLS)
                    mock_save_raw.assert_called_once_with(data)
                    mock_transform.assert_called_once_with(data)
                    mock_save_clean.assert_called_once_with(clean_data)

def test_main_no_data(caplog):
    with patch("src.main.extract_companies_info") as mock_extract:
            mock_extract.return_value = None
    
            with patch("src.main.save_raw_data") as mock_save_raw:
                with patch("src.main.transform_company_data") as mock_transform:
                    with patch("src.main.save_clean_data") as mock_save_clean:
                        main()

                        assert "Pipeline stopped: no data extracted" in caplog.text
    
                        mock_save_raw.assert_not_called()
                        mock_transform.assert_not_called()
                        mock_save_clean.assert_not_called()