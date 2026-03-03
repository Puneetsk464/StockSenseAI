import yfinance as yf
import pandas as pd
from tqdm import tqdm
from symbols import MASTER_STOCK_LIST
import time

stock_data = []
print("Fetching data for the master stock list...")

for sector, caps in MASTER_STOCK_LIST.items():
    for cap_category, tickers in caps.items():
        for ticker_symbol in tqdm(
            tickers, desc=f"Processing {sector} - {cap_category}"
        ):
            try:
                ticker = yf.Ticker(ticker_symbol)
                info = ticker.info

                if info and 'longName' in info:
                    stock_data.append({
                        "Symbol": ticker_symbol,
                        "Name": info.get("longName"),
                        "Sector": sector,
                        "MarketCapCategory": cap_category
                    })

                # Small delay to avoid Yahoo rate limiting
                time.sleep(0.2)

            except Exception:
                print(f"⚠️ Could not fetch data for {ticker_symbol}. Skipping.")

df = pd.DataFrame(stock_data)
df.to_csv("stock_data.csv", index=False)

print(f"\n✅ Success! Data for {len(df)} stocks saved to 'stock_data.csv'.")
