import logging

logger = logging.getLogger(__name__)

def transform_company_data(dataframe):
    dataframe = dataframe.copy()
    duplicates = dataframe.duplicated().sum()
    if duplicates > 0:
        logger.warning(f"{duplicates} duplicate rows found")
        dataframe = dataframe.drop_duplicates()
    invalid_rows = (
        (dataframe["price"] <= 0)
        | (dataframe["marketCap"] <= 0)
        )
    invalid_count = invalid_rows.sum()
    if invalid_count > 0:
        logger.warning(f"{invalid_count} rows with invalid price or marketCap found")
        dataframe = dataframe[~invalid_rows]
    dataframe["marketCap_billions"] = (dataframe["marketCap"] / 1000000000).round(2)

    logger.info("Company data transformation completed")
    return dataframe    