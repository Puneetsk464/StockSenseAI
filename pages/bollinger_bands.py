import streamlit as st

st.set_page_config(page_title="Bollinger Bands Theory", layout="wide")

st.title("Bollinger Bands – Detailed Theory and Concepts")

# BACK BUTTON
if st.button("← Back to Stock Details"):
    st.switch_page("pages/Stock_Details.py")

st.markdown("""
---

# 1. Introduction to Bollinger Bands
Bollinger Bands are a volatility-based technical indicator that creates dynamic price boundaries around a moving average.  
These bands expand during periods of high volatility and contract during periods of low volatility, providing a visual representation of market conditions.

The indicator assists in identifying:
- Overbought and oversold zones  
- Volatility expansions and contractions  
- Potential reversals  
- Breakout opportunities  

---

# 2. Core Components of Bollinger Bands

Bollinger Bands consist of **three separate lines**:

### 2.1 Middle Band  
A **Simple Moving Average (SMA)**, usually set to **20 periods**.  
This line represents the average price over the selected period and acts as the baseline for calculating the upper and lower bands.

### 2.2 Upper Band  
Calculated as:

""")

# formula block for safety
st.markdown(
    "<pre style='background:#0b1220;color:#e6eef8;padding:12px;border-radius:6px;'>"
    "Upper Band = Middle Band + (Standard Deviation × Multiplier)\n"
    "Standard settings: Multiplier = 2"
    "</pre>",
    unsafe_allow_html=True
)

st.markdown("""
This band marks the upper boundary of normal price movement.  
Prices reaching or exceeding this band indicate overextended bullish momentum.

### 2.3 Lower Band  
Calculated as:

""")

st.markdown(
    "<pre style='background:#0b1220;color:#e6eef8;padding:12px;border-radius:6px;'>"
    "Lower Band = Middle Band - (Standard Deviation × Multiplier)"
    "</pre>",
    unsafe_allow_html=True
)

st.markdown("""
This represents the lower boundary of normal price movement.  
Prices touching or falling below this band suggest excessive bearish momentum.

---

# 3. What Standard Deviation Represents
Standard deviation measures **how spread out prices are from the average**.

- High volatility → larger spread → **bands widen**  
- Low volatility → tight price movement → **bands contract**  

This makes Bollinger Bands an adaptive indicator that self-adjusts to market behavior.

---

# 4. How Bollinger Bands Work

## 4.1 Volatility Expansion
When the price becomes highly volatile:  
- Standard deviation increases  
- Upper and lower bands spread apart  
- Market enters a high-energy phase  

This often occurs around news events, breakouts, or trend reversals.

## 4.2 Volatility Contraction (The "Bollinger Squeeze")
When volatility declines:  
- Bands move closer together  
- Standard deviation decreases  
- Market enters consolidation  

A squeeze often precedes a strong breakout, as compressed price action tends to release energy.

---

# 5. Trading Logic Behind Bollinger Bands

Bollinger Bands are built around the concept of **mean reversion**.  
Prices that move too far away from the middle band tend to return toward it.

### 5.1 Mean Reversion Behavior
- Price touches upper band → overextension likely  
- Price touches lower band → undervaluation likely  
- Middle band acts as a magnetic pull  

This behavior forms the core of the strategy used in the project.

---

# 6. Bollinger Band Signals Implemented in the Project

The project uses a classical approach:

### 6.1 Buy Signal: Price touching the Lower Band
Interpretation:
- Selling pressure has reached an extreme  
- Price has fallen rapidly  
- Probability of upward correction increases  

The lower band acts as a zone where bearish momentum may be exhausted.

### 6.2 Sell Signal: Price touching the Upper Band
Interpretation:
- Buying pressure has peaked temporarily  
- Upward momentum may be losing strength  
- Price is stretched above normal volatility range  

This often signals a potential downward move or short-term correction.

---

# 7. Detailed Understanding of Each Component Used in the Strategy

## 7.1 Middle SMA (20-Period Moving Average)
- Smooths out short-term noise  
- Represents the average price over 20 periods  
- Acts as the equilibrium line  
- Often used as a dynamic support or resistance zone  

A 20-period SMA provides a balanced view between short-term and medium-term price behavior.

## 7.2 Standard Deviation
- Measures dispersion of price movements  
- Higher standard deviation → volatile market  
- Lower standard deviation → stable or consolidating market  

Standard deviation is crucial for detecting volatility cycles.

## 7.3 Band Width
Band width is the distance between the upper and lower bands.

High band width:  
- Volatile conditions  
- Frequent breakouts or strong moves  

Low band width:  
- Tight consolidation  
- Possible accumulation or distribution phase  

---

# 8. Why Bollinger Bands Are Effective

### 8.1 Self-Adjusting Indicator
Unlike fixed-range indicators, Bollinger Bands dynamically expand and contract with price behavior.  
This makes them more adaptive to changing market conditions.

### 8.2 Combines Trend and Volatility
The middle band tracks trend direction,  
The outer bands track volatility.

This dual nature allows the indicator to adapt across:
- Trending markets  
- Range-bound markets  
- High-volatility spikes  
- Quiet periods  

### 8.3 Identifies Extremes in Price Behavior
Prices rarely remain outside the bands for long periods.  
Extreme movements outside the bands often revert toward the middle band.

---

# 9. Limitations of Bollinger Bands

### 9.1 Not a Standalone Buy/Sell System
Bands indicate volatility, not direction.  
A touch of the upper band **does not guarantee** reversal downward.  
A touch of the lower band **does not guarantee** reversal upward.

### 9.2 Breakouts Can Be Misleading
During trending markets:
- Price may "walk" the bands  
- Multiple false reversal signals may occur  

### 9.3 Standard Settings May Not Fit All Stocks
Volatile small-cap stocks may require:
- Wider standard deviation (2.5–3.0)  
- Shorter moving average periods  

Large-caps may work well with standard 20-period and 2.0 SD.

---

# 10. Advanced Concepts (Strong for Reviewers)

## 10.1 Bollinger Squeeze Strategy
A sharp contraction of bands signals a potential upcoming breakout.  
Direction is confirmed through:
- Volume spikes  
- Trendlines  
- Moving averages  

## 10.2 Riding the Bands
During strong trends:
- Price frequently closes near the band  
- Staying near the band indicates trend strength  
- Reversals occur only when price pulls away from the band  

## 10.3 Bollinger Band Breakouts
A breakout above the upper band does not indicate overbought conditions;  
Instead, it may signal the start of a strong upward trend.

---

# 11. Parameters Used in This Project

The implementation uses:
- **Period = 20**  
- **Standard deviation = 2.0 for large-caps**  
- **Standard deviation = 2.5 for small-caps**  

This selection balances sensitivity and signal quality.

---

# 12. Summary

Bollinger Bands provide a framework for understanding price volatility and market extremes.

Key points:
- Middle band = 20-period SMA  
- Upper/lower bands = ± standard deviation  
- Bands expand with volatility and contract during calm periods  
- Price touching outer bands signals potential overextension  
- Ideal for mean-reversion strategies  

This indicator is especially effective for visualizing volatility cycles and identifying opportunities created by excessive price movements.

---
""")
