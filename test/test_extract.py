from unittest.mock import patch, MagicMock
from src.extract import extract_company_info
import src.extract 

def test_extract_company_info():
    with patch("src.extract.api_key", "test_api_key"):
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = [{
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "price": 310.34,
                "marketCap": 4558074061040,
                "sector": "Technology",
                "industry": "Consumer Electronics",
                "country": "US",
                "exchange": "NASDAQ"
            }]

            mock_get.return_value = mock_response

            data = extract_company_info("AAPL")

            assert data.iloc[0]["companyName"] == "Apple Inc."
            mock_get.assert_called_once_with(f"https://financialmodelingprep.com/stable/profile?symbol=AAPL", params={"apikey": "test_api_key"}, timeout=10)