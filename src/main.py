from config import logging_config
import logging

from extract import extract_companies_info
from transform import transform_company_data
from load import save_raw_data,save_clean_data

logger = logging.getLogger(__name__)

result = extract_companies_info("aferzfggdf")

if result is None:
    logging.error("Pipeline stopped: no data extracted")
else:
    save_raw_data(result)

    clean_data = transform_company_data(result)

    save_clean_data(clean_data)

    print(clean_data)