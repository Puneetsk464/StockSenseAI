import streamlit as st

st.set_page_config(page_title="SMA Crossover Theory", layout="wide")

st.title("Moving Average Crossover Strategy – Detailed Theory")

# BACK BUTTON
if st.button("← Back to Stock Details"):
    st.switch_page("pages/Stock_Details.py")

st.markdown("""
---

# 1. Introduction to Moving Averages
A moving average (MA) is a statistical method used to smooth price data over a selected period.
It reduces the effect of short-term fluctuations and highlights the overall trend direction.
This smoothing helps in identifying whether the market trend is upward, downward, or sideways.

Two common reasons for using moving averages:
- Price data often contains random noise; averaging creates a cleaner trend profile.
- Trends become easier to visualize and interpret when fluctuations are reduced.

The Moving Average Crossover Strategy uses two Simple Moving Averages (SMAs):
a short-term (fast) SMA and a long-term (slow) SMA.
The relationship between these two lines forms the basis of buy and sell signals.

---

# 2. Simple Moving Average (SMA) Basics

## 2.1 Definition
A Simple Moving Average is the arithmetic mean of closing prices over a fixed period.
Every data point contributes equally.

## Formula (plain text)
The SMA for period N is shown below:

""")

# Use a <pre> block to display the formula cleanly (avoids backtick fences)
st.markdown(
    "<pre style='background:#0b1220;color:#e6eef8;padding:12px;border-radius:6px;'>"
    "SMA = (P1 + P2 + ... + Pn) / N\n\n"
    "Where Pn represents the closing price of each period."
    "</pre>",
    unsafe_allow_html=True,
)

st.markdown("""
This method produces a smooth curve that shows the general direction of price movement.

---

# 3. Fast SMA (Short-Term SMA)

## 3.1 Definition
The fast SMA typically uses shorter periods such as 5, 10, 12, or 20 periods.
Because it averages fewer price points, it reacts quickly to market movements.

## 3.2 Characteristics
- Follows price changes closely.
- Turns upward or downward rapidly.
- Detects trend reversals early.
- Generates more frequent trade signals.

## 3.3 Behavior Explanation
When recent prices rise sharply, the fast SMA increases quickly due to the small averaging window.
When prices fall, it also drops rapidly.
This makes the fast SMA a sensitive indicator of short-term sentiment.

---

# 4. Slow SMA (Long-Term SMA)

## 4.1 Definition
The slow SMA uses larger periods such as 50, 100, or 200 periods.
Because it includes more data points, it reacts gradually to price changes.

## 4.2 Characteristics
- Displays long-term market direction.
- Filters short-term volatility.
- Produces stable, reliable signals.
- Serves as the trend baseline.

## 4.3 Behavior Explanation
If prices change sharply, only a small portion of the slow SMA window is affected.
As a result, the line moves slowly and represents the broader, long-term trend of the security.

---

# 5. Importance of Fast and Slow SMA Together

Using both SMAs allows comparison between short-term and long-term trends.
This relationship is essential because:

- The fast SMA reflects immediate market sentiment.
- The slow SMA reflects the deeper, long-term trend.

When the short-term direction begins to overpower the long-term direction, a crossover occurs, signaling a potential trend shift.

This interaction forms the foundation of the crossover trading approach.

---

# 6. Golden Cross (Buy Signal)

## 6.1 Definition
A Golden Cross occurs when the fast SMA crosses above the slow SMA.

## 6.2 Interpretation
- Short-term price momentum exceeds long-term momentum.
- Buying pressure increases.
- A shift from downward trend to upward trend begins.
- Market sentiment improves.
- Trend reversal towards bullish behavior.

## 6.3 Why It Works
When recent average prices consistently stay above long-term averages, it indicates strength in market demand, often triggering upward movement.

---

# 7. Death Cross (Sell Signal)

## 7.1 Definition
A Death Cross occurs when the fast SMA crosses below the slow SMA.

## 7.2 Interpretation
- Short-term prices weaken compared to long-term prices.
- Selling pressure increases.
- Reversal from upward to downward trend.
- A potential decline phase begins.

## 7.3 Why It Works
If recent prices fall below long-term averages, the market shows signs of weakness and declining momentum.

---

# 8. Mathematical Logic Behind Crossovers

A crossover indicates a change in the relative strength of short-term and long-term averages.

When Fast SMA > Slow SMA:
- Recent average > Long-term average → Uptrend

When Fast SMA < Slow SMA:
- Recent average < Long-term average → Downtrend

The strategy interprets these crossovers as signals for market entries and exits.

---

# 9. Strengths of SMA Crossover Strategy

- Simple to understand and visualize.
- Eliminates emotional decision-making.
- Effective in trending markets.
- Works across multiple asset classes.
- Provides clear entry/exit rules.
- Minimizes guesswork.

---

# 10. Limitations of SMA Crossover Strategy

- Performs poorly in sideways/choppy markets.
- Generates signals with a delay due to averaging.
- May lead to false signals during high volatility.
- Not ideal for very short-term intraday trading.

---

# 11. Why SMA is Used Instead of EMA in This Strategy

- Easier for beginners to understand.
- Produces cleaner, smoother crossovers.
- Less sensitive to sudden intraday spikes.
- Ideal for educational and demonstration purposes.
- Better stability in medium- to long-term periods.

---

# 12. Typical Parameter Choices

Fast SMA periods: 5, 10, 12, 20 — captures short-term price changes and provides early detection of trend shifts.

Slow SMA periods: 20, 50, 100, 200 — represents long-term market direction and filters temporary fluctuations.

These combinations maintain balance between responsiveness and reliability.

---

# 13. Summary

The Moving Average Crossover Strategy uses two SMAs to identify shifts in market momentum.
The fast SMA reflects short-term movements, while the slow SMA reflects long-term trends.
Their crossovers form structured buy and sell signals that help in understanding and participating in trend-based market movements.

---
""")
