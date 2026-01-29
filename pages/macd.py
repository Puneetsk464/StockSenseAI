import streamlit as st

st.set_page_config(page_title="MACD Strategy Theory", page_icon="📘", layout="wide")

# Back button
if st.button("← Back to Stock Details"):
    st.switch_page("pages/Stock_Details.py")

st.title("MACD (Moving Average Convergence Divergence) – Trend & Momentum Indicator")
st.markdown("---")

st.markdown(
    """
## Introduction
MACD, or Moving Average Convergence Divergence, is a trend-following momentum indicator that highlights changes in the strength, direction, and duration of a trend.  
It is widely used because it combines both trend and momentum analysis in one tool.

---

## Core Components of MACD

### 1. MACD Line
The MACD line is calculated as:
- EMA(12) – EMA(26)

The 12-period EMA reacts faster to price changes, while the 26-period EMA moves slower.  
The difference between them represents momentum shifts.

- When EMA(12) stays above EMA(26): upward momentum dominates.
- When EMA(12) stays below EMA(26): downward momentum dominates.

---

### 2. Signal Line
The signal line is a 9-period EMA of the MACD line.  
It smoothens rapid fluctuations to make crossovers easier to interpret.

---

### 3. MACD Histogram
The histogram represents:
- MACD Line – Signal Line

It visually displays momentum strength:
- A positive histogram indicates strengthening bullish momentum.
- A negative histogram indicates strengthening bearish momentum.
- Increasing bar height shows rising momentum.
- Decreasing bar height shows weakening momentum.

---

## MACD Signals

### Bullish Crossover
Occurs when the MACD line crosses above the signal line.  
Indicates strengthening upward momentum.  
Often used as a buy signal.

---

### Bearish Crossover
Occurs when the MACD line crosses below the signal line.  
Indicates decreasing upward momentum or increasing downward momentum.  
Often used as a sell or exit signal.

---

### Zero-Line Crossovers
The zero line divides positive and negative momentum.

- MACD crossing above zero suggests a shift into an uptrend.
- MACD crossing below zero suggests a shift into a downtrend.

Zero-line crossovers confirm broader trend direction.

---

### Divergence (Advanced)
Divergence occurs when MACD and price move in opposite directions.

- Bullish Divergence:  
  Price makes lower lows, but MACD makes higher lows → possible upward reversal.
  
- Bearish Divergence:  
  Price makes higher highs, but MACD makes lower highs → possible downward reversal.

Divergences indicate weakening trends.

---

## Why MACD Is Effective
MACD works well because:
- It reacts quickly using EMAs.
- It visualizes momentum through the histogram.
- It identifies trend reversals early.
- It combines multiple signals in one indicator.

This makes it useful in both short-term and medium-term trading.

---

## Limitations of MACD
- Lagging indicator due to EMA calculations.
- Generates false signals in sideways or choppy markets.
- Divergence requires experience to interpret accurately.
- Works best when combined with support/resistance or volume analysis.

---

## Ideal Market Conditions
MACD performs well in:
- Trending markets
- Steady momentum phases
- Medium volatility environments

MACD struggles in:
- Sideways price movement
- Low-volume assets
- Highly volatile spikes

---

## Summary Table

| Component | Explanation |
|----------|-------------|
| MACD Line | Measures the difference between fast and slow EMAs |
| Signal Line | Smoothed version of MACD for clearer signals |
| Histogram | Visual representation of momentum strength |
| Zero Line | Boundary separating bullish and bearish zones |

---

## Key Takeaways
- MACD identifies momentum and trend direction.
- Crossovers provide entry and exit signals.
- Histogram reveals strength of momentum shifts.
- Best when combined with other confirmations.

"""
)


