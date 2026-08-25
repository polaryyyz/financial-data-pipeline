from config import logging_config
from extract import extract_companies_info
from transform import transform_company_data
from load import save_raw_data,save_clean_data

result = extract_companies_info("AAPL", "MSFT", "NVDA")

save_raw_data(result)

clean_data = transform_company_data(result)

save_clean_data(clean_data)

print(clean_data)