# StockSenseAI: Your Personal Investment Strategist

StockSenseAI is an **AI-assisted stock analysis and strategy backtesting platform** built as a **Final Year Engineering Project**.

The platform focuses on **visual, explainable, and educational analysis of stock market data** while allowing users to:

* Analyze stocks using technical indicators
* Build and test trading strategies
* Validate strategies across historical market conditions
* Receive AI-based portfolio recommendations based on risk profile

The system is designed as a **learning-oriented investment analysis tool** that combines **technical analysis, backtesting, and AI-driven portfolio personalization**.

---

# 🚀 Features

### 📈 Real-Time Market Data

* Live stock price tracking
* Intraday charts with 5-minute intervals
* Day high / low monitoring

### 📊 Historical Analysis

* Interactive historical price charts
* Line charts and candlestick charts
* Adjustable time windows (1M – Max)

### 🔬 Strategy Builder & Backtesting Lab

Users can **combine multiple technical indicators** to create custom trading strategies.

The system generates:

* Buy/Sell signals
* Backtesting simulation
* Strategy performance metrics
* Historical validation across market windows

### 🧠 AI-Based Portfolio Recommendation (PPM)

A machine learning module analyzes user financial data and generates **risk-adjusted portfolio recommendations**.

---

# 🔬 Strategy Builder & Backtesting Engine

The **Advanced Strategy Lab** allows users to create custom trading strategies using multiple indicators simultaneously.

Users can select:

* Moving Averages
* RSI
* MACD
* Bollinger Bands

The system combines signals from selected indicators and executes simulated trades using a **virtual capital backtesting engine**.

---

# 📚 Implemented Trading Indicators

## 1️⃣ Moving Average Crossover (Trend Following)

Uses two moving averages:

* Short-term SMA
* Long-term SMA

Signals:

BUY → Short MA crosses above Long MA
SELL → Short MA crosses below Long MA

Best suited for **trending markets**.

---

## 2️⃣ Relative Strength Index – RSI (Momentum)

Momentum oscillator ranging from **0 – 100**.

Key levels:

Oversold → Below 30
Overbought → Above 70

Best suited for **range-bound markets**.

---

## 3️⃣ Bollinger Bands (Volatility)

Three-band volatility indicator:

Middle Band → 20 period SMA
Upper Band → +2 Standard Deviations
Lower Band → −2 Standard Deviations

Used to identify **volatility expansion and reversal zones**.

---

## 4️⃣ MACD (Trend & Momentum)

Moving Average Convergence Divergence uses:

MACD Line = EMA(12) − EMA(26)
Signal Line = EMA(9 of MACD)

Signals are generated using **MACD crossovers and histogram momentum**.

---

# 📊 Strategy Evaluation

Every strategy run produces:

* Buy/Sell signal markers
* Strategy return %
* Number of trades executed
* Win rate
* Final portfolio value
* Comparison with Buy & Hold strategy

---

# 📉 Historical Strategy Validation

To test **strategy robustness**, the system splits the historical dataset into multiple **validation windows**.

Each window shows:

* Time period
* Number of trades
* Strategy return

This helps evaluate if a strategy works consistently across **different market conditions** rather than only one time range.

---

# 🤖 AI Portfolio Personalization Module (PPM)

The **Portfolio Personalization Module (PPM)** generates stock portfolio recommendations based on user financial profile.

User inputs:

* Age
* Annual income
* Investment corpus
* Investment horizon
* Risk appetite
* Investment goal

---

## Risk Score Calculation

A **normalized risk score (0–1)** is computed using weighted factors.

Example:

Risk Score = **0.72**

Risk category is then determined:

| Risk Score | Category     |
| ---------- | ------------ |
| 0 – 0.3    | Conservative |
| 0.3 – 0.6  | Balanced     |
| 0.6 – 1.0  | Growth       |

---

## Portfolio Recommendation Engine

Based on the risk category, the system selects and weights stocks using:

* Historical return analysis
* Volatility filtering
* Sector diversification
* Portfolio optimization

---

# 🧠 Machine Learning Models Used

### Random Forest Regressor

Used for predicting expected stock returns.

Features include:

* Historical returns
* Volatility
* Momentum indicators
* Moving averages
* Sector performance

Random Forest was selected because it performs well on **non-linear financial datasets**.

---

# 📊 Data Sources

Stock market data is fetched using:

**Yahoo Finance API (`yfinance`)**

Data includes:

* OHLC price data
* Volume
* Historical price movements

---

# 🛠️ Tech Stack

### Programming Language

Python

### Framework

Streamlit

### Data Processing

Pandas
NumPy

### Visualization

Plotly

### Machine Learning

Scikit-learn

### Market Data

Yahoo Finance API (yfinance)

---

# 📂 Project Structure

```
StockSenseAI/
│
├── Home.py
│
├── pages/
│   ├── Companies.py
│   ├── Stock_Details.py
│   ├── Strategy_Lab_Advanced.py
│   ├── ma_crossover.py
│   ├── rsi.py
│   ├── bollinger_bands.py
│   ├── macd.py
│   ├── PPM_Login.py
│   ├── PPM_Profile.py
│   └── PPM_Dashboard.py
│
├── ppm/
│   ├── risk_model.py
│   ├── stock_model.py
│   ├── portfolio_optimizer.py
│   ├── projection_model.py
│   └── universe_builder.py
│
├── fetch_data.py
├── firebase_config.py
├── sector_map.py
│
├── requirements.txt
└── README.md
```

---

# ▶️ How to Run

### 1️⃣ Clone the Repository

```
git clone https://github.com/yourusername/StockSenseAI.git
cd StockSenseAI
```

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```
streamlit run Home.py
```

---

# 🎯 Project Status

**Active Development**

Current modules implemented:

* Stock analysis dashboard
* Technical indicator visualizations
* Advanced strategy builder
* Backtesting engine
* Historical validation windows
* AI-based portfolio recommendation (PPM)

---

# ⚠️ Disclaimer

This project is built **for educational and research purposes only**.

It does **not provide financial advice or investment recommendations**.
