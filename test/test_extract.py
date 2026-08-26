from unittest.mock import patch, MagicMock, call
from src.extract import extract_company_info
from src.extract import extract_companies_info
import src.extract 
import requests

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

def test_extract_company_info_no_data():
    with patch("src.extract.api_key", "test_api_key"):
            with patch("requests.get") as mock_get:
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = []
    
                mock_get.return_value = mock_response

                data = extract_company_info("AAPL")

                assert data is None

def test_extract_company_info_http_error():
    with patch("src.extract.api_key", "test_api_key"):
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock(side_effect = requests.exceptions.HTTPError())

            mock_get.return_value = mock_response

            data = extract_company_info("AAPL")

            assert data is None

def test_extract_company_info_timeout_error():
    with patch("src.extract.api_key", "test_api_key"):
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout

            data = extract_company_info("AAPL")

            assert data is None

def test_extract_company_info_conection_error():
    with patch("src.extract.api_key", "test_api_key"):
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError

            data = extract_company_info("AAPL")

            assert data is None

def test_extract_company_info_request_exception():
    with patch("src.extract.api_key", "test_api_key"):
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException

            data = extract_company_info("AAPL")

            assert data is None

def test_extract_companies_info():
    with patch("src.extract.api_key", "test_api_key"):
        with patch("requests.get") as mock_get:
            mock_response_1 = MagicMock()
            mock_response_1.json.return_value = [{
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "price": 310.34,
                "marketCap": 4558074061040,
                "sector": "Technology",
                "industry": "Consumer Electronics",
                "country": "US",
                "exchange": "NASDAQ"
            }]

            mock_response_2 = MagicMock()
            mock_response_2.json.return_value = [{
                "symbol": "MSFT",
                "companyName": "Microsoft Corporation",
                "price": 487.31,
                "marketCap": 3618544770500,
                "sector": "Technology",
                "industry": "Software - Infrastructure",
                "country": "US",
                "exchange": "NASDAQ"
            }]

            mock_get.side_effect = [mock_response_1, mock_response_2]

            data = extract_companies_info("AAPL", "MSFT")

            assert data.iloc[0]["companyName"] == "Apple Inc."
            assert data.iloc[1]["companyName"] == "Microsoft Corporation"
            mock_get.assert_has_calls([
                call(f"https://financialmodelingprep.com/stable/profile?symbol=AAPL", params={"apikey": "test_api_key"}, timeout=10),
                call(f"https://financialmodelingprep.com/stable/profile?symbol=MSFT", params={"apikey": "test_api_key"}, timeout=10)
                ])

def test_extract_companies_info_no_data():
    with patch("src.extract.api_key", "test_api_key"):
        with patch("requests.get") as mock_get:
            mock_response_1 = MagicMock()
            mock_response_1.json.return_value = []

            mock_response_2 = MagicMock()
            mock_response_2.json.return_value = []

            mock_get.side_effect = [mock_response_1, mock_response_2]

            data = extract_companies_info("AAPL", "MSFT")

            assert data is None

def test_extract_companies_info_missing_data():
    with patch("src.extract.api_key", "test_api_key"):
        with patch("requests.get") as mock_get:
            mock_response_1 = MagicMock()
            mock_response_1.json.return_value = [{
                "symbol": "AAPL",
                "companyName": "Apple Inc.",
                "price": 310.34,
                "marketCap": 4558074061040,
                "sector": "Technology",
                "industry": "Consumer Electronics",
                "country": "US",
                "exchange": "NASDAQ"
            }]

            mock_response_2 = MagicMock()
            mock_response_2.json.return_value = []

            mock_get.side_effect = [mock_response_1, mock_response_2]

            data = extract_companies_info("AAPL", "MSFT")

            assert data.iloc[0]["companyName"] == "Apple Inc."
            assert len(data) == 1
            mock_get.assert_has_calls([
                call(f"https://financialmodelingprep.com/stable/profile?symbol=AAPL", params={"apikey": "test_api_key"}, timeout=10),
                call(f"https://financialmodelingprep.com/stable/profile?symbol=MSFT", params={"apikey": "test_api_key"}, timeout=10)
                ])