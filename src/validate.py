import logging

logger = logging.getLogger(__name__)


def validate_company_data(dataframe):
    required_columns = [
        "symbol",
        "companyName",
        "price",
        "marketCap",
        "sector",
        "industry",
        "country",
        "exchange",
        "marketCap_billions",
    ]

    if dataframe.empty:
        raise ValueError("Dataset is empty")

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    if dataframe["symbol"].duplicated().any():
        raise ValueError("Duplicate symbols found")

    if (dataframe["price"] <= 0).any():
        raise ValueError("Invalid prices found")

    if (dataframe["marketCap"] <= 0).any():
        raise ValueError("Invalid market caps found")

    logger.info("Company data validation completed successfully")