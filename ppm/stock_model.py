import yfinance as yf
import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

from ppm.universe_builder import get_symbol_list


# --------------------------------
# Indicator Functions
# --------------------------------

def compute_rsi(series, window=14):

    delta = series.diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


def compute_macd(series):

    ema12 = series.ewm(span=12).mean()
    ema26 = series.ewm(span=26).mean()

    macd = ema12 - ema26

    return macd


# --------------------------------
# Feature Engineering
# --------------------------------

def create_features(df):

    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()

    df["RSI"] = compute_rsi(df["Close"])

    df["MACD"] = compute_macd(df["Close"])

    df["Volatility"] = df["Close"].pct_change().rolling(20).std()

    df["Momentum"] = df["Close"].pct_change(10)

    return df


# --------------------------------
# Create Target Variable
# --------------------------------

def create_target(df, horizon_days=30):

    df["future_return"] = (
        df["Close"].shift(-horizon_days) - df["Close"]
    ) / df["Close"]

    return df


# --------------------------------
# Build Training Dataset
# --------------------------------

def build_dataset():

    symbols = get_symbol_list()

    all_data = []

    for symbol in symbols:

        try:

            df = yf.download(symbol, period="5y", progress=False)

            if len(df) < 200:
                continue

            df = create_features(df)

            df = create_target(df)

            df = df.dropna()

            features = df[[
                "SMA20",
                "SMA50",
                "RSI",
                "MACD",
                "Volatility",
                "Momentum"
            ]]

            target = df["future_return"]

            dataset = pd.concat([features, target], axis=1)

            all_data.append(dataset)

        except Exception as e:
            print("Error downloading", symbol)

    final_df = pd.concat(all_data)

    return final_df


# --------------------------------
# Train Model
# --------------------------------

def train_model():

    print("Building dataset...")

    df = build_dataset()

    X = df.drop("future_return", axis=1)
    y = df["future_return"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4
    )

    print("Training model...")

    model.fit(X_train, y_train)

    joblib.dump(model, "models/stock_model.pkl")

    print("Stock model trained and saved.")


# --------------------------------

if __name__ == "__main__":
    train_model()