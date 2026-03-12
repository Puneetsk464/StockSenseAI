import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Advanced Strategy Lab", layout="wide")

# ---------------------------------------------------------
# GET SELECTED STOCK
# ---------------------------------------------------------

ticker = st.session_state.get("selected_stock")

if not ticker:
    st.error("Please select a stock first from the Companies page.")
    st.stop()

st.title(f"Advanced Strategy Builder — {ticker}")

# ---------------------------------------------------------
# TIME FILTER
# ---------------------------------------------------------

period = st.radio(
    "Select Time Period",
    ["3M","6M","1Y","3Y","5Y"],
    horizontal=True
)

period_map = {
    "3M":"3mo",
    "6M":"6mo",
    "1Y":"1y",
    "3Y":"3y",
    "5Y":"5y"
}

df = yf.download(ticker, period=period_map[period], progress=False)

if isinstance(df.columns,pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df.dropna(inplace=True)

# ---------------------------------------------------------
# OPTIMAL PARAMETERS
# ---------------------------------------------------------

if period=="3M":
    ma_short,ma_long = 5,15
elif period=="6M":
    ma_short,ma_long = 8,21
elif period=="1Y":
    ma_short,ma_long = 20,50
else:
    ma_short,ma_long = 50,200

# ---------------------------------------------------------
# INDICATOR SELECTION
# ---------------------------------------------------------

st.subheader("Select Indicators")

c1,c2,c3,c4 = st.columns(4)

with c1:
    use_ma = st.checkbox("Moving Average")

with c2:
    use_rsi = st.checkbox("RSI")

with c3:
    use_macd = st.checkbox("MACD")

with c4:
    use_bb = st.checkbox("Bollinger Bands")

# indicator summary
selected=[]
if use_ma: selected.append("MA")
if use_rsi: selected.append("RSI")
if use_macd: selected.append("MACD")
if use_bb: selected.append("BB")

if selected:
    st.caption("Active Indicators: " + ", ".join(selected))

# Set threshold based on number of indicators (no slider needed)
num_indicators = len(selected)
if num_indicators == 0:
    threshold = 1
elif num_indicators == 1:
    threshold = 1  # Single indicator: all signals pass
else:
    threshold = 2  # Multiple indicators: require agreement (2+)

st.divider()

# ---------------------------------------------------------
# INDICATOR CALCULATIONS
# ---------------------------------------------------------

if use_ma:
    df["MA_short"]=df["Close"].rolling(ma_short).mean()
    df["MA_long"]=df["Close"].rolling(ma_long).mean()

if use_rsi:

    delta=df["Close"].diff()
    gain=delta.clip(lower=0)
    loss=-delta.clip(upper=0)

    avg_gain=gain.rolling(14).mean()
    avg_loss=loss.rolling(14).mean()

    rs=avg_gain/avg_loss
    df["RSI"]=100-(100/(1+rs))

if use_macd:

    ema12=df["Close"].ewm(span=12).mean()
    ema26=df["Close"].ewm(span=26).mean()

    df["MACD"]=ema12-ema26
    df["MACD_signal"]=df["MACD"].ewm(span=9).mean()

if use_bb:

    df["BB_mid"]=df["Close"].rolling(20).mean()
    std=df["Close"].rolling(20).std()

    df["BB_upper"]=df["BB_mid"]+2*std
    df["BB_lower"]=df["BB_mid"]-2*std

# ---------------------------------------------------------
# SIGNAL GENERATION
# ---------------------------------------------------------

buy=[]
sell=[]

for i in range(len(df)):

    signals=[]

    if use_ma and i>0:
        if df["MA_short"].iloc[i] > df["MA_long"].iloc[i]:
            signals.append(1)
        else:
            signals.append(-1)

    if use_rsi and not np.isnan(df["RSI"].iloc[i]):
        if df["RSI"].iloc[i]<30:
            signals.append(1)
        elif df["RSI"].iloc[i]>70:
            signals.append(-1)
        # Skip neutral zone (30-70) - no vote

    if use_macd and not np.isnan(df["MACD"].iloc[i]):
        if df["MACD"].iloc[i] > df["MACD_signal"].iloc[i]:
            signals.append(1)
        else:
            signals.append(-1)

    if use_bb and not np.isnan(df["BB_lower"].iloc[i]):
        if df["Close"].iloc[i] < df["BB_lower"].iloc[i]:
            signals.append(1)
        elif df["Close"].iloc[i] > df["BB_upper"].iloc[i]:
            signals.append(-1)
        # Skip middle zone (within bands) - no vote

    # Count only actual votes (1 or -1)
    buy_votes = signals.count(1)
    sell_votes = signals.count(-1)

    # Generate signals based on vote agreement
    if buy_votes >= threshold and buy_votes > sell_votes:
        buy.append(1)
        sell.append(0)
    elif sell_votes >= threshold and sell_votes > buy_votes:
        buy.append(0)
        sell.append(1)
    else:
        buy.append(0)
        sell.append(0)

df["Buy"]=buy
df["Sell"]=sell

# ---------------------------------------------------------
# BACKTEST
# ---------------------------------------------------------

cash=10000
shares=0
portfolio=[]

for i in range(len(df)):

    price=df["Close"].iloc[i]

    if df["Buy"].iloc[i]==1 and cash>0:
        shares=cash/price
        cash=0

    elif df["Sell"].iloc[i]==1 and shares>0:
        cash=shares*price
        shares=0

    value=cash + shares*price
    portfolio.append(value)

df["Portfolio"]=portfolio

# ---------------------------------------------------------
# CHART
# ---------------------------------------------------------

st.subheader("Strategy Backtest Visualization")

fig=go.Figure()

fig.add_trace(go.Candlestick(
    x=df.index,
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"],
    name="Price"
))

if use_ma:
    fig.add_trace(go.Scatter(x=df.index,y=df["MA_short"],name=f"MA {ma_short}"))
    fig.add_trace(go.Scatter(x=df.index,y=df["MA_long"],name=f"MA {ma_long}"))

if use_bb:
    fig.add_trace(go.Scatter(x=df.index,y=df["BB_upper"],name="BB Upper"))
    fig.add_trace(go.Scatter(x=df.index,y=df["BB_lower"],name="BB Lower"))

buy_pts=df[df["Buy"]==1]
sell_pts=df[df["Sell"]==1]

fig.add_trace(go.Scatter(
    x=buy_pts.index,
    y=buy_pts["Close"],
    mode="markers",
    marker=dict(color="green",size=10),
    name="Buy"
))

fig.add_trace(go.Scatter(
    x=sell_pts.index,
    y=sell_pts["Close"],
    mode="markers",
    marker=dict(color="red",size=10),
    name="Sell"
))

fig.update_layout(height=550)
fig.update_xaxes(rangeslider_visible=False)

st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------------
# PERFORMANCE METRICS
# ---------------------------------------------------------

initial=10000
final=df["Portfolio"].iloc[-1]

ret=((final-initial)/initial)*100

trades=int(df["Buy"].sum())

wins=np.sum(np.diff(df["Portfolio"])>0)

win_rate=(wins/len(df))*100

st.subheader("Strategy Performance")

c1,c2,c3,c4=st.columns(4)

c1.metric("Return",f"{ret:.2f}%")
c2.metric("Trades",trades)
c3.metric("Win Rate",f"{win_rate:.1f}%")
c4.metric("Final Value",f"₹{final:,.0f}")

# ---------------------------------------------------------
# HISTORICAL WINDOWS
# ---------------------------------------------------------

st.subheader("Historical Performance Validation")

# Map periods to days for window calculations
period_days_map = {
    "3M": 90,
    "6M": 180,
    "1Y": 365,
    "3Y": 365*3,
    "5Y": 365*5
}

# Download longer history for backtesting multiple windows
download_map = {
    "3M": "2y",   # 2 years = ~8 x 3M windows
    "6M": "2y",   # 2 years = 4 x 6M windows
    "1Y": "5y",   # 5 years = 5 x 1Y windows
    "3Y": "10y",  # 10 years
    "5Y": "10y"   # 10 years
}

# Downloads longer historical data for window analysis
hist_df = yf.download(ticker, period=download_map[period], progress=False)

if isinstance(hist_df.columns, pd.MultiIndex):
    hist_df.columns = hist_df.columns.get_level_values(0)

hist_df.dropna(inplace=True)

# Split into contiguous, non-overlapping windows going backwards
window_days = period_days_map[period]
windows_list = []

# Start from the most recent date and work backwards in contiguous blocks
most_recent_date = hist_df.index[-1]
current_end = most_recent_date

while len(windows_list) < 6:
    current_start = current_end - pd.Timedelta(days=window_days)

    # Get data for this window
    window_data = hist_df[(hist_df.index >= current_start) &
                          (hist_df.index <= current_end)]

    if len(window_data) < 20:  # Skip if insufficient data
        break

    # Run the strategy on this window
    # Recreate indicators for this window
    window_df = window_data.copy()

    if use_ma:
        window_df["MA_short"] = window_df["Close"].rolling(ma_short).mean()
        window_df["MA_long"] = window_df["Close"].rolling(ma_long).mean()

    if use_rsi:
        delta = window_df["Close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()
        rs = avg_gain / avg_loss
        window_df["RSI"] = 100 - (100 / (1 + rs))

    if use_macd:
        ema12 = window_df["Close"].ewm(span=12).mean()
        ema26 = window_df["Close"].ewm(span=26).mean()
        window_df["MACD"] = ema12 - ema26
        window_df["MACD_signal"] = window_df["MACD"].ewm(span=9).mean()

    if use_bb:
        window_df["BB_mid"] = window_df["Close"].rolling(20).mean()
        std = window_df["Close"].rolling(20).std()
        window_df["BB_upper"] = window_df["BB_mid"] + 2 * std
        window_df["BB_lower"] = window_df["BB_mid"] - 2 * std

    # Generate signals for this window
    buy = []
    sell = []

    for i in range(len(window_df)):
        signals = []

        if use_ma and i > 0:
            if window_df["MA_short"].iloc[i] > window_df["MA_long"].iloc[i]:
                signals.append(1)
            else:
                signals.append(-1)

        if use_rsi and not np.isnan(window_df["RSI"].iloc[i]):
            if window_df["RSI"].iloc[i] < 30:
                signals.append(1)
            elif window_df["RSI"].iloc[i] > 70:
                signals.append(-1)
            # Skip neutral zone (30-70) - no vote

        if use_macd and not np.isnan(window_df["MACD"].iloc[i]):
            if window_df["MACD"].iloc[i] > window_df["MACD_signal"].iloc[i]:
                signals.append(1)
            else:
                signals.append(-1)

        if use_bb and not np.isnan(window_df["BB_lower"].iloc[i]):
            if window_df["Close"].iloc[i] < window_df["BB_lower"].iloc[i]:
                signals.append(1)
            elif window_df["Close"].iloc[i] > window_df["BB_upper"].iloc[i]:
                signals.append(-1)
            # Skip middle zone (within bands) - no vote

        # Count only actual votes (1 or -1)
        buy_votes = signals.count(1)
        sell_votes = signals.count(-1)

        # Generate signals based on vote agreement
        if buy_votes >= threshold and buy_votes > sell_votes:
            buy.append(1)
            sell.append(0)
        elif sell_votes >= threshold and sell_votes > buy_votes:
            buy.append(0)
            sell.append(1)
        else:
            buy.append(0)
            sell.append(0)

    window_df["Buy"] = buy
    window_df["Sell"] = sell

    # Backtest on this window
    cash = 10000
    shares = 0
    portfolio = []

    for i in range(len(window_df)):
        price = window_df["Close"].iloc[i]

        if window_df["Buy"].iloc[i] == 1 and cash > 0:
            shares = cash / price
            cash = 0
        elif window_df["Sell"].iloc[i] == 1 and shares > 0:
            cash = shares * price
            shares = 0

        value = cash + shares * price
        portfolio.append(value)

    window_df["Portfolio"] = portfolio

    # Calculate window performance
    start_val = window_df["Portfolio"].iloc[0]
    end_val = window_df["Portfolio"].iloc[-1]

    if start_val > 0:
        window_ret = ((end_val - start_val) / start_val) * 100
    else:
        window_ret = 0

    start_date = window_df.index[0].strftime("%d %b %Y")
    end_date = window_df.index[-1].strftime("%d %b %Y")
    trades = int(window_df["Buy"].sum())

    windows_list.append({
        "period": f"{start_date} → {end_date}",
        "return": window_ret,
        "trades": trades
    })

    # Move to previous window (contiguous, non-overlapping)
    current_end = current_start - pd.Timedelta(days=1)

# Reverse to show chronologically (oldest to newest)
windows_list.reverse()

# Display window cards
cols = st.columns(min(len(windows_list), 4))

for i, w in enumerate(windows_list[-4:]):  # Show last 4 windows
    color = "green" if w["return"] > 0 else "red"

    with cols[i]:
        st.markdown(
            f"""
            <div style="padding:15px;border-radius:10px;border:1px solid #333;background:#111;">
            <h4 style="font-size:12px;">{w['period']}</h4>
            <p style="margin:5px 0;">Trades: {w['trades']}</p>
            <p style="font-size:24px;color:{color};margin:10px 0;">
            {w['return']:.2f}%
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write(f"*Showing last 4 windows of {period} each*")


# ---------------------------------------------------------
# WINDOW CHART
# ---------------------------------------------------------

if windows_list:
    chart_df = pd.DataFrame(windows_list)

    fig2 = px.bar(
        chart_df,
        x="period",
        y="return",
        title=f"Strategy Stability Across {period} Historical Windows",
        color="return",
        color_continuous_scale=["#EF4444", "#FBBF24", "#10B981"]
    )

    fig2.update_layout(
        xaxis_title="Time Period",
        yaxis_title="Return (%)",
        height=400,
        template="plotly_white"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.info(
        f"✓ Strategy tested on {len(windows_list)} historical {period} windows. "
        f"Stable performance across windows = robust strategy"
    )


# ---------------------------------------------------------
# STRATEGY COMPARISON
# ---------------------------------------------------------

st.subheader("Strategy Comparison")

strategies={
    "Combined Strategy":ret,
    "Buy & Hold":((df["Close"].iloc[-1]-df["Close"].iloc[0])/df["Close"].iloc[0])*100
}

cols=st.columns(len(strategies))

for i,(name,val) in enumerate(strategies.items()):

    color="green" if val>0 else "red"

    with cols[i]:

        st.markdown(
        f"""
        <div style="padding:15px;border-radius:10px;border:1px solid #333;background:#111;">
        <h4>{name}</h4>
        <p style="font-size:24px;color:{color}">
        {val:.2f}%
        </p>
        </div>
        """,
        unsafe_allow_html=True
        )