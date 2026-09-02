import pandas as pd

from src.transform import transform_company_data

def test_remove_duplicates():
    data = pd.DataFrame(
        {
            "symbol": ["AAPL", "AAPL"],
            "companyName": ["Apple Inc.", "Apple Inc."],
            "price": [310.34, 310.34],
            "marketCap": [4558074061040, 4558074061040],
            "sector": ["Technology", "Technology"],
            "industry": ["Consumer Electronics", "Consumer Electronics"],
            "country": ["US", "US"],
            "exchange": ["NASDAQ", "NASDAQ"]
        }
    )

    result = transform_company_data(data)

    assert len(result) == 1

def test_remove_invalid_values():
    data = pd.DataFrame(
        {
            "symbol": ["AAPL", "MSFT", "NVDA"],
            "companyName": ["Apple Inc.", "Microsoft Corporation", "NVIDIA Corporation"],
            "price": [310.34, -10, 208.48],
            "marketCap": [4558074061040, 3618544770500, 0],
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

    result = transform_company_data(data)

    assert len(result) == 1
    assert result.iloc[0]["symbol"] == "AAPL"

def test_market_cap_conversion():
    data = pd.DataFrame(
        {
            "symbol": ["AAPL"],
            "companyName": ["Apple Inc."],
            "price": [310.34],
            "marketCap": [4558074061040],
            "sector": ["Technology"],
            "industry": ["Consumer Electronics"],
            "country": ["US"],
            "exchange": ["NASDAQ"]
        }
    )

    result = transform_company_data(data)

    assert result.iloc[0]["marketCap_billions"] == 4558.07