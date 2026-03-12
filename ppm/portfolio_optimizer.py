import joblib
import yfinance as yf
import pandas as pd
import numpy as np
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ---------------- LOAD MODEL ----------------

try:
    model = joblib.load("models/stock_model.pkl")
    logger.info(f"✓ Model loaded successfully. Expected features: {model.n_features_in_}")
except Exception as e:
    logger.error(f"✗ Failed to load model: {e}")
    raise


# ---------------- LOAD STOCK UNIVERSE ----------------

def load_stock_universe():

    df = pd.read_csv("stock_data.csv")

    df = df.rename(columns={
        "Symbol": "symbol",
        "Sector": "sector",
        "MarketCapCategory": "market_cap"
    })

    logger.info(f"Universe size: {len(df)}")

    return df.to_dict("records")


# ---------------- INDICATORS ----------------

def compute_rsi(series, window=14):

    delta = series.diff()

    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()

    rs = gain / loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


def compute_macd(series):

    ema12 = series.ewm(span=12).mean()
    ema26 = series.ewm(span=26).mean()

    return ema12 - ema26


# ---------------- FEATURE ENGINEERING ----------------

def build_features(df):

    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()

    df["RSI"] = compute_rsi(df["Close"])

    df["MACD"] = compute_macd(df["Close"])

    df["Volatility"] = df["Close"].pct_change().rolling(20).std()

    df["Momentum"] = df["Close"].pct_change(10)

    return df


# ---------------- PREDICT RETURNS ----------------

def predict_stock_returns():

    universe = load_stock_universe()
    logger.info(f"Starting predictions for {len(universe)} stocks")

    predictions = []

    for stock in universe:

        symbol = stock["symbol"]

        try:

            df = yf.download(
                symbol,
                period="1y",
                progress=False,
                auto_adjust=True,
                threads=False
            )

            if df is None or df.empty:
                logger.debug(f"  {symbol} - No data from Yahoo Finance")
                continue

            if len(df) < 60:
                logger.debug(f"  {symbol} - Insufficient data: {len(df)} days (need 60+)")
                continue

            # Flatten MultiIndex columns from yfinance
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df = build_features(df)

            latest = df.iloc[-1][[
                "SMA20",
                "SMA50",
                "RSI",
                "MACD",
                "Volatility",
                "Momentum"
            ]]

            # FIX: fill missing indicator values instead of skipping stock
            latest = latest.fillna(0)

            # Convert Series to dict then to DataFrame to avoid tuple column names
            latest_df = pd.DataFrame([latest.to_dict()])

            # Debug: Check feature names and shape
            logger.debug(f"  {symbol} - Features: {list(latest_df.columns)}, Shape: {latest_df.shape}")

            predicted_return = model.predict(latest_df)[0]

            volatility = df["Close"].pct_change().std()

            if volatility is None or volatility == 0 or np.isnan(volatility):
                volatility = 0.0001

            predictions.append({
                "symbol": symbol,
                "sector": stock["sector"],
                "market_cap": stock["market_cap"],
                "predicted_return": predicted_return,
                "volatility": volatility
            })
            logger.debug(f"  {symbol} - ✓ Prediction successful")

        except Exception as e:
            logger.warning(f"  {symbol} - ✗ {type(e).__name__}: {str(e)}")
            continue

    df_pred = pd.DataFrame(predictions)

    logger.info(f"Prediction complete. Stocks with predictions: {len(df_pred)}")

    return df_pred


# ---------------- PORTFOLIO OPTIMIZER ----------------

def build_portfolio(risk_category):

    df = predict_stock_returns()

    if df.empty:
        logger.warning("No predictions generated")
        return pd.DataFrame()

    df = df.sort_values("predicted_return", ascending=False)

    # Compute average volatility for the dataset
    avg_volatility = df["volatility"].median()

    # Compute Sharpe-like score for risk assessment
    sharpe_score = df["predicted_return"] / (df["volatility"] + 0.0001)

    # ---------------- RISK-BASED FILTERS ----------------

    if risk_category == "Conservative":
        # Low risk: Large cap, low volatility, steady returns
        df = df[df["market_cap"] == "Large Cap"]
        df = df[df["volatility"] <= avg_volatility]
        df = df.sort_values("predicted_return", ascending=True)  # Stable over high return
        logger.info(f"Conservative filter: {len(df)} stocks (Large Cap, volatility <= {avg_volatility:.6f})")

    elif risk_category == "Moderate":
        # Medium risk: Large + Mid cap, medium volatility
        df = df[df["market_cap"].isin(["Large Cap", "Mid Cap"])]
        df = df[df["volatility"] <= avg_volatility * 1.2]
        df = df.sort_values("predicted_return", ascending=False)  # Balance return and risk
        logger.info(f"Moderate filter: {len(df)} stocks (Large/Mid Cap, volatility <= {avg_volatility * 1.2:.6f})")

    elif risk_category == "Growth":
        # Higher risk: All cap sizes, moderate-high volatility, high returns
        df = df[df["volatility"] <= avg_volatility * 1.5]
        df = df.sort_values("predicted_return", ascending=False)  # Prefer high returns
        logger.info(f"Growth filter: {len(df)} stocks (volatility <= {avg_volatility * 1.5:.6f})")

    elif risk_category == "Aggressive":
        # High risk: All cap sizes, no volatility limit, highest returns
        df = df.sort_values("predicted_return", ascending=False)  # Maximize returns
        logger.info(f"Aggressive filter: {len(df)} stocks (all market caps, no volatility limit)")

    logger.info(f"After risk filter: {len(df)} stocks")

    if df.empty:
        logger.warning(f"No {risk_category} stocks available after filtering")
        return pd.DataFrame()

    # ---------------- SECTOR DIVERSIFICATION ----------------

    # Risk-aware portfolio sizing
    portfolio_size = {
        "Conservative": 10,  # More diversified for stability
        "Moderate": 8,
        "Growth": 6,
        "Aggressive": 5  # Concentrated for higher returns
    }
    target_size = portfolio_size.get(risk_category, 8)

    portfolio = []
    used_sectors = set()

    for _, row in df.iterrows():

        if row["sector"] not in used_sectors:

            portfolio.append(row)

            used_sectors.add(row["sector"])

        if len(portfolio) >= target_size:
            break

    portfolio_df = pd.DataFrame(portfolio)

    logger.info(f"After diversification: {len(portfolio_df)} stocks (target={target_size})")

    if portfolio_df.empty:
        logger.warning("No stocks after sector diversification")
        return pd.DataFrame()

    # ---------------- SHARPE-LIKE SCORE ----------------

    portfolio_df["score"] = (
        portfolio_df["predicted_return"] /
        (portfolio_df["volatility"] + 0.0001)
    )

    portfolio_df["score"] = portfolio_df["score"].replace(
        [np.inf, -np.inf], np.nan)
    portfolio_df["score"] = portfolio_df["score"].fillna(0)

    # Risk-aware weight allocation
    total_score = portfolio_df["score"].sum()

    if risk_category == "Conservative":
        # Equal-weight for stability and predictability
        portfolio_df["weight"] = 1 / len(portfolio_df)
        logger.debug("Conservative: Using equal-weight allocation")

    elif risk_category == "Moderate":
        # Balanced weight based on Sharpe ratio
        if total_score == 0:
            portfolio_df["weight"] = 1 / len(portfolio_df)
        else:
            portfolio_df["weight"] = portfolio_df["score"] / total_score
        logger.debug("Moderate: Using Sharpe-based weight allocation")

    elif risk_category == "Growth":
        # Favor higher scores more strongly
        portfolio_df["score"] = portfolio_df["score"] ** 1.3
        total_score = portfolio_df["score"].sum()
        if total_score == 0:
            portfolio_df["weight"] = 1 / len(portfolio_df)
        else:
            portfolio_df["weight"] = portfolio_df["score"] / total_score
        logger.debug("Growth: Using exponential-weight allocation (favors high scores)")

    elif risk_category == "Aggressive":
        # Heavily concentrate on highest scores
        portfolio_df["score"] = portfolio_df["score"] ** 2.0
        total_score = portfolio_df["score"].sum()
        if total_score == 0:
            portfolio_df["weight"] = 1 / len(portfolio_df)
        else:
            portfolio_df["weight"] = portfolio_df["score"] / total_score
        logger.debug("Aggressive: Using concentrated allocation (heavily favors high scores)")

    portfolio_df = portfolio_df.reset_index(drop=True)

    logger.info(f"Final portfolio size: {len(portfolio_df)} stocks")

    return portfolio_df
