import os
import pandas as pd
import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("FMP_API_KEY")

def extract_company_info(symbol):
    url = f"https://financialmodelingprep.com/stable/profile?symbol={symbol}"
    params = {
        "apikey": "gGUVAg4SH6a4CI5VEAwief5i8KvkkFNv"
    }
    r = requests.get(url, params=params)
    data = r.json()
    all_info = pd.DataFrame(data)
    essential = all_info[["symbol", "companyName", "price", "marketCap", "sector", "industry", "country", "exchange"]]

    return essential

def extract_companies_info(*args):
    essential = []
    for symbol in args:
        symbols = extract_company_info(symbol)
        essential.append(symbols)
    all_df = pd.concat(essential, ignore_index=True)
    return all_df


print(extract_companies_info("AAPL", "MSFT", "NVDA"))
