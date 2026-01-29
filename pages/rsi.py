import streamlit as st

st.set_page_config(page_title="RSI Theory", layout="wide")

st.title("Relative Strength Index (RSI) – Detailed Theory and Concepts")

# BACK BUTTON
if st.button("← Back to Stock Details"):
    st.switch_page("pages/Stock_Details.py")

st.markdown("""
---

# 1. Introduction to RSI
The Relative Strength Index (RSI) is a momentum indicator designed to measure the speed and magnitude of recent price changes.  
It identifies overbought and oversold levels in a market, allowing the detection of potential reversals.

RSI is widely used in swing trading, short-term trading, and mean-reversion strategies.

---

# 2. Purpose of RSI
RSI helps interpret whether a price move is strong, weak, or overstretched.  
The indicator compresses price momentum into a scale from **0 to 100**, making it easy to interpret:

- Very high RSI → price has moved upward too quickly  
- Very low RSI → price has dropped too quickly  

This creates natural zones for identifying potential reversals.

---

# 3. Understanding Momentum
Momentum refers to the **rate at which price changes**.  
RSI measures momentum using the relationship between **average gains** and **average losses** within a user-defined lookback period (commonly 14 periods).

- Strong upward momentum = repeated gains → RSI rises  
- Strong downward momentum = repeated losses → RSI falls  

Momentum often shifts **before** price does, giving RSI its predictive ability.

---

# 4. How RSI is Calculated (Beginner-Friendly Explanation)

RSI uses these steps:

### Step 1: Calculate Price Change
Price change = Current Close − Previous Close  
Positive → gain  
Negative → loss  

### Step 2: Separate Gains and Losses
All positive differences become **gains**  
All negative differences (absolute values) become **losses**

### Step 3: Compute Averages
Calculate the average gain and average loss across the chosen period (usually 14).

### Step 4: Compute Relative Strength (RS)
RS = Average Gain ÷ Average Loss

### Step 5: Convert RS into RSI
Shown below using a `<pre>` block:

""")

# Formula block using <pre> for safe rendering
st.markdown(
    "<pre style='background:#0b1220;color:#e6eef8;padding:12px;border-radius:6px;'>"
    "RSI = 100 - (100 / (1 + RS))\n"
    "Where RS = (Average Gain) / (Average Loss)"
    "</pre>",
    unsafe_allow_html=True,
)

st.markdown("""
---

# 5. Standard RSI Levels and Meaning

### 5.1 Overbought Zone (Above 70)
- Indicates strong upward momentum  
- Buying pressure may be exhausting  
- Price may be overextended  
- A reversal or pullback often follows

### 5.2 Oversold Zone (Below 30)
- Indicates strong downward momentum  
- Selling pressure may be fading  
- Price may be undervalued in the short term  
- A reversal upward is common

### 5.3 Neutral Zone (Between 30–70)
- Normal trading activity  
- No extreme buying or selling pressure  
- Often represents consolidation phases

---

# 6. RSI Signals in Trading Strategies

## 6.1 Buy Signal (RSI crossing upward from oversold zone)
Occurs when RSI rises above the oversold threshold (e.g., from 25 → 30).

Interpretation:
- Downtrend may be ending  
- Selling pressure has weakened  
- Momentum is shifting upward  

## 6.2 Sell Signal (RSI crossing downward from overbought zone)
Occurs when RSI falls below the overbought threshold (e.g., from 75 → 70).

Interpretation:
- Uptrend may be ending  
- Price has risen too quickly  
- Momentum is shifting downward  

---

# 7. Why RSI Works (Conceptual Logic)

### 7.1 Mean Reversion Principle
Financial prices often revert toward the average after extreme moves.  
RSI identifies those extreme conditions.

### 7.2 Behavioral Explanation
Investors tend to:
- Overreact during rallies  
- Panic during declines  

This creates quickly-stretched price moves, which RSI captures.

### 7.3 Momentum Exhaustion
When RSI is too high or too low:
- Buying or selling energy becomes exhausted  
- Reversals or consolidations follow  

These weakening conditions appear in RSI **before** price changes direction.

---

# 8. RSI Settings Used in This Project

The implementation uses:
- **Default period = 14**
- **Oversold threshold = 30**
- **Overbought threshold = 70**

For more volatile stocks, adjustments are applied:
- Oversold can be lowered to 25  
- Overbought can be raised to 75  

This allows RSI to adapt better to stocks with large swings.

---

# 9. RSI Strengths

### 9.1 Works well in ranging markets
RSI is excellent when price oscillates between support and resistance.

### 9.2 Easy to read and interpret
The 0–100 scale simplifies understanding.

### 9.3 Helps identify turning points
Momentum reversals often occur before price reversals.

### 9.4 Useful for short-term trading
Ideal for swing traders and intraday traders using 5–14 period RSI.

---

# 10. RSI Limitations (Very Important)

### 10.1 Poor performance in trending markets
RSI may stay overbought or oversold for extended periods, giving early or false signals.

### 10.2 Can generate noise in high-volatility stocks
Rapid spikes can distort RSI values.

### 10.3 Oversold ≠ guaranteed bounce  
Oversold conditions indicate weakness but not a guaranteed reversal.

### 10.4 Needs confirmation
Works best with:
- Support/resistance  
- Trendlines  
- Moving averages  
- Volume  

---

# 11. RSI Divergence (Advanced but important)

Although not implemented directly in this project, divergence is important theory.

### Bullish Divergence
Price makes lower lows  
RSI makes higher lows  
→ Downtrend weakening  
→ Possible upward reversal  

### Bearish Divergence
Price makes higher highs  
RSI makes lower highs  
→ Uptrend weakening  
→ Possible downward reversal  

---

# 12. Practical Example (Beginner-Friendly)

Consider a constant drop in price for 10 candles:
- Most candles have losses → high average loss  
- Gains are almost zero → low average gain  
- RS becomes very small  
- RSI falls below 30 → oversold  

This indicates selling pressure may be exhausted.

If price begins to stabilize:
- Losses reduce  
- Gains start appearing  
- RS begins rising  
- RSI crosses above 30 → trend strength improving  
→ A buy signal is created  

---

# 13. Summary

The Relative Strength Index measures the strength and speed of price changes.  
By comparing average gains and losses, it provides a numerical measure of momentum.

Key insights:
- RSI < 30 → oversold  
- RSI > 70 → overbought  
- Rising RSI indicates increasing momentum  
- Falling RSI indicates weakening momentum  

The indicator is best suited for mean-reversion strategies and works well in sideways markets.

---
""")
