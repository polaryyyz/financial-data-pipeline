import os
import pandas as pd
import requests
import logging.config
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

config = {
     "version": 1,
     "formatters": {
         "standard": {
             "format": '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
     },
     "handlers": {
         "file": {
               "class": "logging.FileHandler",
               "filename": "logs/pipeline.log",
               "level": "DEBUG",
               "formatter": "standard"
          },
          "console": {
               "class": "logging.StreamHandler",
               "stream": "ext://sys.stdout",
               "level": "INFO",
               "formatter": "standard"
          },
    },
     "root": {
         "level": "DEBUG",
         "handlers": ["file", "console"]
        }         
}
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

#logging.basicConfig(
#                level = logging.DEBUG,
#                format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                filename = "logs/pipeline.log"
#            )

api_key = os.getenv("FMP_API_KEY")

#Extraction

def extract_company_info(symbol):
    try:
        logger.debug(f"Starting extraction for: {symbol}")
        url = f"https://financialmodelingprep.com/stable/profile?symbol={symbol}"
        params = {
        "apikey": api_key
        }
        r = requests.get(url, params=params, timeout=10)
        logger.debug(f"Request sent for: {symbol}")
        r.raise_for_status()
        logger.debug(f"Response received with status {r.status_code} for {symbol}")
        data = r.json()
        if not data:
            logger.warning(f"No data found for: {symbol}")
            return None
        all_info = pd.DataFrame(data)
        essential = all_info[["symbol", "companyName", "price", "marketCap", "sector", "industry", "country", "exchange"]]
        logger.info(f"Successfully extracted data for: {symbol}")

        return essential

    
    except requests.exceptions.HTTPError as http_error:
        logger.error(f"HTTP Error for {symbol}: {http_error}")
        
    except requests.exceptions.Timeout as timeout:
        logger.error(f"API is too slow for {symbol}: {timeout}")

    except requests.exceptions.ConnectionError as connection_error:
        logger.error(f"Connection issue for {symbol}: {connection_error}")

    except requests.exceptions.RequestException as request_except:
        logger.error(f"Request exception for {symbol}: {request_except}")

def save_raw_data(dataframe):
    try: 
        output_path = Path("data/raw/company_data.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        dataframe.to_csv(output_path, index=False)
        logger.info(f"File creation completed: {output_path}")

    except OSError as os_err:
        logger.error(f"Error with entry/output {os_err}")

def extract_companies_info(*args):
    essential = []
    for company_info in args:
            company_df = extract_company_info(company_info)
            if company_df is not None:
                essential.append(company_df)
    if not essential:
        logger.warning(f"No data found for requested symbols: {args}") 
        return None            
    all_df = pd.concat(essential, ignore_index=True)
    save_raw_data(all_df)
    return all_df
    
result = extract_companies_info("AAPL", "afegdgssdg", "NVDA")
print(result)