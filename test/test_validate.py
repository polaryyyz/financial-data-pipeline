import pandas as pd 
import pytest
from src.validate import validate_company_data

def valid_dataframe():
    return pd.DataFrame(
        {
            "symbol": ["AAPL", "MSFT"],
            "companyName": ["Apple", "Microsoft"],
            "price": [200.0, 400.0],
            "marketCap": [3_000_000_000_000, 2_500_000_000_000],
            "sector": ["Technology", "Technology"],
            "industry": ["Consumer Electronics", "Software"],
            "country": ["US", "US"],
            "exchange": ["NASDAQ", "NASDAQ"],
            "marketCap_billions": [3000.0, 2500.0],
        }
    )

def test_validate_company_data_success():
    dataframe = valid_dataframe()

    validate_company_data(dataframe)


def test_validate_company_data_empty():
    dataframe = pd.DataFrame()

    with pytest.raises(ValueError, match="Dataset is empty"):
        validate_company_data(dataframe)


def test_validate_company_data_missing_column():
    dataframe = valid_dataframe().drop(columns=["price"])

    with pytest.raises(ValueError, match="Missing columns"):
        validate_company_data(dataframe)


def test_validate_company_data_duplicate_symbol():
    dataframe = valid_dataframe()
    dataframe.loc[1, "symbol"] = "AAPL"

    with pytest.raises(ValueError, match="Duplicate symbols found"):
        validate_company_data(dataframe)

def test_validate_company_data_invalid_price():
    dataframe = valid_dataframe()
    dataframe.loc[0, "price"] = 0

    with pytest.raises(ValueError, match="Invalid prices found"):
        validate_company_data(dataframe)


def test_validate_company_data_invalid_market_cap():
    dataframe = valid_dataframe()
    dataframe.loc[0, "marketCap"] = 0

    with pytest.raises(ValueError, match="Invalid market caps found"):
        validate_company_data(dataframe)