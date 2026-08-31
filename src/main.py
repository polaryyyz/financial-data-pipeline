from src.config import logging_config
from src.config.symbols import SYMBOLS
import logging

from src.extract import extract_companies_info
from src.transform import transform_company_data
from src.load import save_raw_data,save_clean_data

def main():
    result = extract_companies_info(*SYMBOLS)

    if result is None:
        logging.error("Pipeline stopped: no data extracted")
        return

    save_raw_data(result)

    clean_data = transform_company_data(result)

    save_clean_data(clean_data)

    print(clean_data)

if __name__ == "__main__":
    main()