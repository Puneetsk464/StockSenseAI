import yfinance as yf
import pandas as pd
from tqdm import tqdm
from symbols import MASTER_STOCK_LIST

stock_data = []
print("Fetching data for the master stock list...")

for sector, caps in MASTER_STOCK_LIST.items():
    for cap_category, tickers in caps.items():
        for ticker_symbol in tqdm(tickers, desc=f"Processing {sector} - {cap_category}"):
            try:
                info = yf.Ticker(ticker_symbol).info
                if 'longName' in info:
                    stock_data.append({
                        'Symbol': ticker_symbol,
                        'Name': info.get('longName'),
                        'Sector': sector,
                        'MarketCapCategory': cap_category
                    })
            except Exception:
                print(f"\nCould not fetch data for {ticker_symbol}. Skipping.")

df = pd.DataFrame(stock_data)
output_path = 'stock_data.csv'
df.to_csv(output_path, index=False)

print(f"\n✅ Success! Data for {len(df)} stocks saved to '{output_path}'.")