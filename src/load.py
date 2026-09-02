import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def save_raw_data(dataframe):
    try: 
        output_path = Path("data/raw/company_data.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        dataframe.to_csv(output_path, index=False)
        logger.info(f"File creation completed: {output_path}")

    except OSError as os_err:
        logger.error(f"Error with input/output: {os_err}")

def save_clean_data(dataframe):
    try: 
        output_path = Path("data/processed/company_data_clean.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        dataframe.to_csv(output_path, index=False)
        logger.info(f"Clean file creation completed: {output_path}")

    except OSError as os_err:
        logger.error(f"Error with input/output: {os_err}")
        raise