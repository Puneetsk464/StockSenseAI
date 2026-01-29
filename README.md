# StockSenseAI

StockSenseAI is an AI-powered stock market analysis and strategy backtesting platform built as a Final Year Engineering project.  
The system focuses on visual, explainable, and educational analysis of stock market data using technical indicators and trading strategies.

---

## 🚀 Features

- 📈 Real-time stock price tracking with intraday charts
- 📊 Historical stock price visualization (Line & Candlestick)
- 🧠 Strategy-based technical analysis with clear signal overlays
- 🔁 Backtesting engine with performance comparison
- 🎓 Beginner-friendly explanations of indicators and strategies

---

## 📚 Implemented Trading Strategies

### 1. Moving Average Crossover (Trend Following)
- Uses fast and slow Simple Moving Averages (SMA)
- Buy/Sell signals generated on crossover events
- Best suited for trending markets

### 2. Relative Strength Index – RSI (Momentum)
- Momentum oscillator ranging from 0 to 100
- Identifies overbought and oversold conditions
- Effective in range-bound markets

### 3. Bollinger Bands (Volatility)
- Uses standard deviation around a moving average
- Identifies volatility expansion and contraction
- Suitable for volatile and sideways markets

### 4. MACD (Trend & Momentum)
- Combines trend-following and momentum concepts
- Uses EMA crossovers and histogram analysis
- Helps confirm trend direction and strength

---

## 📊 Strategy Evaluation

Each strategy includes:
- Buy/Sell signal generation
- Visual overlays on historical price charts
- Backtesting with virtual capital
- Performance comparison with Buy & Hold strategy
- Explanation of why the strategy performed well or poorly

---

## 🛠️ Tech Stack

- **Language:** Python
- **Framework:** Streamlit
- **Data Source:** Yahoo Finance (yfinance)
- **Visualization:** Plotly
- **Data Handling:** Pandas, NumPy

---

## 📂 Project Structure

StockSenseAI/
│
├── Home.py
├── pages/
│ ├── Companies.py
│ ├── Stock_Details.py
│ ├── ma_crossover.py
│ ├── rsi.py
│ ├── bollinger_bands.py
│ └── macd.py
│
├── assets/
├── requirements.txt
└── README.md


---

## ▶️ How to Run

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
    pip install -r requirements.txt

4. Run the application:
    streamlit run Home.py

---

## 🎯 Project Status

**Ongoing**  
Future work includes:
- Machine learning–based signal generation
- User authentication and personalization
- Recommendation system
- Advanced forecasting models

---

## ⚠️ Disclaimer

This project is for educational purposes only and does not provide financial advice.
