import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="Stock Details", page_icon="📊",
                   layout="wide", initial_sidebar_state="collapsed")

# --- BACK BUTTON ---
if st.button("← Back to Companies"):
    st.switch_page("pages/Companies.py")

st.divider()

# --- SESSION VARIABLES ---
selected_ticker = st.session_state.get("selected_ticker")
if not selected_ticker:
    st.error("No stock selected. Please go back and select a company.")
    st.stop()

try:
    ticker = yf.Ticker(selected_ticker)
    info = ticker.info
    stock_name = info.get('longName', selected_ticker)
except Exception as e:
    st.error(f"Could not fetch initial data for {selected_ticker}: {e}")
    st.stop()

st.title(f"📊 {stock_name}")
st.caption(f"Symbol: {selected_ticker}")
st.divider()

# --------------------------------------------------------------------
# SECTION 1: LIVE REFRESHING VIEW
# --------------------------------------------------------------------
st.subheader("🔴 Real-Time View")
live_placeholder = st.empty()

# --------------------------------------------------------------------
# SECTION 2: HISTORICAL DATA
# --------------------------------------------------------------------
st.divider()
st.subheader("🔬 Historical Price Chart")

filter_col1, filter_col2 = st.columns([3, 2])
with filter_col1:
    periods = {"1M": "1mo", "3M": "3mo", "6M": "6mo", "1Y": "1y", "Max": "max"}
    selected_period_label = st.radio(
        "Select Period:", options=list(periods.keys()), horizontal=True)
with filter_col2:
    hist_chart_type = st.radio(
        "Chart Type:", ["Line", "Candlestick"], horizontal=True, key="hist_chart_type")

try:
    hist_df = ticker.history(period=periods[selected_period_label])
    if hist_df.empty:
        st.warning(f"No historical data found for {selected_period_label}.")
    else:
        if hist_chart_type == 'Line':
            hist_fig = px.line(hist_df, x=hist_df.index, y="Close",
                               title=f"{stock_name} Closing Price ({selected_period_label})")
        else:
            hist_fig = go.Figure(
                data=[go.Candlestick(
                    x=hist_df.index,
                    open=hist_df['Open'], high=hist_df['High'],
                    low=hist_df['Low'], close=hist_df['Close']
                )]
            )
            hist_fig.update_layout(
                title_text=f"{stock_name} OHLC ({selected_period_label})")

        hist_fig.update_layout(
            height=500, hovermode="x unified", margin=dict(l=20, r=20, t=40, b=20))
        hist_fig.update_xaxes(rangeslider_visible=False)
        st.plotly_chart(hist_fig, use_container_width=True)

        with st.expander("View Historical Data Table"):
            st.dataframe(hist_df.sort_index(ascending=False))
except Exception as e:
    st.error(f"Could not fetch historical data: {e}")

# --------------------------------------------------------------------
# ENHANCED SECTION 3: STRATEGY ANALYSIS (EDUCATIONAL FOCUS)
# --------------------------------------------------------------------
st.divider()
st.subheader("🎓 Strategy Analysis & Education")

# Strategy selection with better descriptions
strategy = st.selectbox(
    "Learn & Analyze Trading Strategies:",
    [
        "Moving Average Crossover (Trend Following)",
        "Relative Strength Index - RSI (Momentum)",
        "Bollinger Bands (Volatility)",
        "MACD (Trend & Momentum) - Coming Soon"
    ],
    index=0
)

# --- STRATEGY THEORY & EDUCATION SECTION ---
st.markdown("---")
st.subheader("📚 Strategy Theory & Concepts")

# Educational note about strategy performance
st.info("""
**Note:** Real-world results can vary based on market conditions. 
Sometimes RSI works better on large caps, and MA crossovers on small caps. 
This demonstrates how market context affects strategy performance.
""")

if strategy == "Moving Average Crossover (Trend Following)":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Understanding Moving Average Crossovers
        
        **Concept:**
        Uses two moving averages to identify trend changes. When the shorter-term average crosses the longer-term average, it signals potential trend reversals.
        
        **Trading Signals:**
        - **BUY**: Short-term SMA crosses above long-term SMA (Golden Cross)
        - **SELL**: Short-term SMA crosses below long-term SMA (Death Cross)
        
        **Best For:** Trending markets with clear directional bias
        **Challenges:** Sideways or choppy markets create false signals
        """)
    with col2:
        st.info("""
        **Optimal Settings:**
        - Short-term: 5-20 periods
        - Long-term: 20-200 periods
        - Longer periods reduce false signals
        """)

elif strategy == "Relative Strength Index - RSI (Momentum)":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Understanding RSI (Relative Strength Index)
        
        **Concept:**
        Momentum oscillator measuring the speed and change of price movements. Ranges from 0-100, indicating overbought and oversold conditions.
        
        **Key Levels:**
        - **Oversold (Below 30)**: Potential buying opportunity
        - **Overbought (Above 70)**: Potential selling opportunity
        
        **Trading Signals:**
        - Buy when RSI crosses above oversold level
        - Sell when RSI crosses below overbought level
        
        **Best For:** Ranging markets with clear support/resistance
        **Challenges:** Strong trending markets create false signals
        """)
    with col2:
        st.info("""
        **Optimal Settings:**
        - Period: 14 (standard)
        - Oversold: 25-35
        - Overbought: 65-75
        """)

elif strategy == "Bollinger Bands (Volatility)":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Understanding Bollinger Bands
        
        **Concept:**
        Volatility-based indicator using standard deviations around a moving average to identify overbought/oversold conditions.
        
        **Components:**
        - Middle Band: 20-period Simple Moving Average
        - Upper Band: Middle + (2 × Standard Deviation)
        - Lower Band: Middle - (2 × Standard Deviation)
        
        **Trading Signals:**
        - Buy when price touches lower band + confirmation
        - Sell when price touches upper band + confirmation
        
        **Best For:** Volatile, ranging markets
        **Challenges:** Strong breakouts and low volatility periods
        """)
    with col2:
        st.info("""
        **Optimal Settings:**
        - Period: 20 days
        - Std Dev: 2.0 (standard)
        - Excellent for volatile small caps
        """)

# --- INTERACTIVE PARAMETERS SECTION ---
st.markdown("---")
st.subheader("⚙️ Strategy Parameters & Configuration")

# Optimal parameters based on period and stock type
def get_optimal_parameters(period, strategy_name, ticker_symbol):
    """Return optimal parameters based on period and strategy"""
    
    # Detect if it's a small cap stock
    small_cap_indicators = ['RBLBANK', 'J&KBANK', 'UCOBANK', 'SOUTHBANK', 'KTKBANK']
    is_small_cap = any(indicator in ticker_symbol for indicator in small_cap_indicators)
    
    if strategy_name == "Moving Average Crossover (Trend Following)":
        if period == "1M":
            return {"short": 5, "long": 15, "investment": 10000}
        elif period == "3M":
            return {"short": 8, "long": 21, "investment": 10000}
        elif period == "6M":
            return {"short": 12, "long": 26, "investment": 10000}
        elif period == "1Y":
            return {"short": 20, "long": 50, "investment": 10000}
        else:  # Max
            return {"short": 50, "long": 200, "investment": 10000}
    
    elif strategy_name == "Relative Strength Index - RSI (Momentum)":
        if is_small_cap:
            # More sensitive settings for volatile small caps
            return {"period": 12, "oversold": 28, "overbought": 72, "investment": 10000}
        else:
            # Standard settings for large/mid caps
            return {"period": 14, "oversold": 30, "overbought": 70, "investment": 10000}
    
    elif strategy_name == "Bollinger Bands (Volatility)":
        if is_small_cap:
            # Wider bands for volatile small caps
            return {"period": 20, "std_dev": 2.5, "investment": 10000}
        else:
            # Standard settings
            return {"period": 20, "std_dev": 2.0, "investment": 10000}

# Get optimal parameters
optimal_params = get_optimal_parameters(selected_period_label, strategy, selected_ticker)

if strategy == "Moving Average Crossover (Trend Following)":
    st.info("Optimal settings pre-selected based on historical performance for this timeframe")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        short_window = st.slider("Short-term SMA", 2, 50, optimal_params["short"],
                               help="Faster reaction to price changes - more signals")
    with col2:
        long_window = st.slider("Long-term SMA", 10, 200, optimal_params["long"],
                              help="Shows overall trend direction - fewer false signals")
    with col3:
        investment = st.number_input("Simulation Investment (₹)", 1000, 1000000, optimal_params["investment"], 1000,
                                   help="Virtual amount to test strategy performance")

elif strategy == "Relative Strength Index - RSI (Momentum)":
    st.info("Settings optimized for this stock type and timeframe")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        rsi_period = st.slider("RSI Period", 5, 21, optimal_params["period"],
                             help="Standard is 14 periods. Shorter = more sensitive")
    with col2:
        rsi_oversold = st.slider("Oversold Level", 10, 40, optimal_params["oversold"],
                               help="Buy when RSI crosses above this level")
    with col3:
        rsi_overbought = st.slider("Overbought Level", 60, 90, optimal_params["overbought"],
                                 help="Sell when RSI crosses below this level")
    
    investment = st.number_input("Simulation Investment (₹)", 1000, 1000000, optimal_params["investment"], 1000)

elif strategy == "Bollinger Bands (Volatility)":
    st.info("Perfect for volatile stocks - captures breakouts and reversals")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        bb_period = st.slider("Bollinger Period", 10, 30, optimal_params["period"],
                            help="Moving average period for the middle band")
    with col2:
        bb_std = st.slider("Standard Deviations", 1.0, 3.0, optimal_params["std_dev"], 0.1,
                         help="Higher values = wider bands, fewer signals")
    with col3:
        investment = st.number_input("Simulation Investment (₹)", 1000, 1000000, optimal_params["investment"], 1000)

# --- STRATEGY EXECUTION & BACKTESTING ---
st.markdown("---")
st.subheader("🔍 Strategy Analysis & Backtesting")

if st.button("🎯 Run Strategy Analysis", type="primary", use_container_width=True):
    with st.spinner("Analyzing strategy performance and generating insights..."):
        
        if strategy == "Moving Average Crossover (Trend Following)":
            # --- Compute SMAs & Signals ---
            hist_df[f"SMA_{short_window}"] = hist_df['Close'].rolling(window=short_window).mean()
            hist_df[f"SMA_{long_window}"] = hist_df['Close'].rolling(window=long_window).mean()
            hist_df['Signal'] = 0
            hist_df.loc[hist_df.index[long_window:], 'Signal'] = (
                hist_df[f"SMA_{short_window}"][long_window:] > hist_df[f"SMA_{long_window}"][long_window:]
            ).astype(int)
            hist_df['Position'] = hist_df['Signal'].diff()

            buy_signals = hist_df[hist_df['Position'] == 1]
            sell_signals = hist_df[hist_df['Position'] == -1]

            # --- Plot Strategy Visualization ---
            st.subheader("Strategy Visualization")
            
            if hist_chart_type == 'Line':
                strat_fig = go.Figure()
                strat_fig.add_trace(go.Scatter(
                    x=hist_df.index, y=hist_df['Close'], name="Close Price", line=dict(color='white', width=2)))
                strat_fig.add_trace(go.Scatter(
                    x=hist_df.index, y=hist_df[f"SMA_{short_window}"], name=f"SMA {short_window}", 
                    line=dict(color='#F59E0B', width=1.5)))
                strat_fig.add_trace(go.Scatter(
                    x=hist_df.index, y=hist_df[f"SMA_{long_window}"], name=f"SMA {long_window}", 
                    line=dict(color='#8B5CF6', width=1.5)))
                strat_fig.add_trace(go.Scatter(
                    x=buy_signals.index, y=buy_signals['Close'], mode='markers',
                    marker=dict(color='#10B981', symbol='triangle-up', size=12, line=dict(width=2, color='white')),
                    name='Buy Signal'))
                strat_fig.add_trace(go.Scatter(
                    x=sell_signals.index, y=sell_signals['Close'], mode='markers',
                    marker=dict(color='#EF4444', symbol='triangle-down', size=12, line=dict(width=2, color='white')),
                    name='Sell Signal'))
            else:
                strat_fig = go.Figure(data=[go.Candlestick(
                    x=hist_df.index,
                    open=hist_df['Open'], high=hist_df['High'],
                    low=hist_df['Low'], close=hist_df['Close'],
                    name="Price"
                )])
                strat_fig.add_trace(go.Scatter(
                    x=hist_df.index, y=hist_df[f"SMA_{short_window}"], name=f"SMA {short_window}", 
                    line=dict(color='#F59E0B', width=2)))
                strat_fig.add_trace(go.Scatter(
                    x=hist_df.index, y=hist_df[f"SMA_{long_window}"], name=f"SMA {long_window}", 
                    line=dict(color='#8B5CF6', width=2)))
                strat_fig.add_trace(go.Scatter(
                    x=buy_signals.index, y=buy_signals['Close'], mode='markers',
                    marker=dict(color='#10B981', symbol='triangle-up', size=10),
                    name='Buy Signal'))
                strat_fig.add_trace(go.Scatter(
                    x=sell_signals.index, y=sell_signals['Close'], mode='markers',
                    marker=dict(color='#EF4444', symbol='triangle-down', size=10),
                    name='Sell Signal'))

            strat_fig.update_layout(
                title=f"MA Crossover Strategy: {stock_name}",
                height=500, 
                hovermode="x unified", 
                margin=dict(l=20, r=20, t=40, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            strat_fig.update_xaxes(rangeslider_visible=False)
            st.plotly_chart(strat_fig, use_container_width=True)

            # --- Backtest Simulation ---
            cash = investment
            shares = 0
            trades = []
            
            for i in range(len(hist_df)):
                if hist_df['Position'].iloc[i] == 1 and cash > 0:  # Buy signal
                    shares = cash / hist_df['Close'].iloc[i]
                    cash = 0
                    trades.append({'date': hist_df.index[i], 'action': 'BUY', 'price': hist_df['Close'].iloc[i]})
                elif hist_df['Position'].iloc[i] == -1 and shares > 0:  # Sell signal
                    cash = shares * hist_df['Close'].iloc[i]
                    shares = 0
                    trades.append({'date': hist_df.index[i], 'action': 'SELL', 'price': hist_df['Close'].iloc[i]})

            final_value = cash + (shares * hist_df['Close'].iloc[-1])
            profit_percent = ((final_value - investment) / investment) * 100
            
            # Buy & Hold comparison
            buy_hold_value = investment * (hist_df['Close'].iloc[-1] / hist_df['Close'].iloc[0])
            buy_hold_percent = ((buy_hold_value - investment) / investment) * 100

            # --- RESULTS DISPLAY ---
            st.success("Strategy Analysis Completed!")
            
            # Performance Metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Strategy Return", f"{profit_percent:.2f}%", delta=f"{profit_percent:.2f}%")
            col2.metric("Buy & Hold Return", f"{buy_hold_percent:.2f}%", delta=f"{buy_hold_percent:.2f}%")
            col3.metric("Total Trades", len(trades))
            col4.metric("Final Value", f"₹{final_value:,.2f}")

            # --- PERFORMANCE ANALYSIS ---
            st.markdown("---")
            st.subheader("Performance Analysis")

            price_change = ((hist_df['Close'].iloc[-1] - hist_df['Close'].iloc[0]) / hist_df['Close'].iloc[0]) * 100
            success_rate = (len([t for t in trades if t['action'] == 'SELL']) / len(trades) * 100) if trades else 0

            if profit_percent > buy_hold_percent and profit_percent > 0:
                st.success("**Strategy Outperformed Buy & Hold**")
                st.write(f"**Performance:** +{profit_percent:.1f}% vs Buy & Hold +{buy_hold_percent:.1f}%")
                
                if price_change > 10:
                    st.write("""
                    **Why it worked:**
                    - Strong trending market created ideal conditions
                    - Clear directional moves allowed precise timing
                    - Strategy captured majority of upward movement
                    - Effective trend identification and following
                    """)
                else:
                    st.write("""
                    **Why it worked:**
                    - Active trading generated returns despite limited movement
                    - Multiple successful position rotations
                    - Effective timing of market fluctuations
                    - Outperformed in sideways or volatile conditions
                    """)

            elif profit_percent > 0:
                st.warning("**Strategy Underperformed Buy & Hold**")
                st.write(f"**Performance:** +{profit_percent:.1f}% vs Buy & Hold +{buy_hold_percent:.1f}%")
                
                st.write("""
                **Performance factors:**
                - Challenging market conditions for trend identification
                - Transaction costs affected overall returns
                - Missed portions of major price moves
                - Sideways action created false signals
                """)

            else:
                st.error("**Strategy Resulted in Loss**")
                st.write(f"**Performance:** {profit_percent:.1f}% vs Buy & Hold +{buy_hold_percent:.1f}%")
                
                if abs(price_change) < 5:
                    st.write("""
                    **Why it struggled:**
                    - Non-trending market generated false crossovers
                    - Frequent whipsaw action caused repeated losses
                    - Transaction costs accumulated without significant movement
                    - Lack of clear directional bias
                    """)
                else:
                    st.write("""
                    **Why it struggled:**
                    - High volatility disrupted trend identification
                    - Poor timing of entries and exits
                    - Failed to adapt to changing market conditions
                    - Missed major directional moves
                    """)

            # Market Context
            st.markdown("**Market Context**")
            context_col1, context_col2, context_col3 = st.columns(3)
            context_col1.metric("Price Change", f"{price_change:+.1f}%")
            context_col2.metric("Success Rate", f"{success_rate:.1f}%" if trades else "N/A")
            context_col3.metric("Performance Gap", f"{profit_percent - buy_hold_percent:+.1f}%")

            # Educational Insights
            st.markdown("**Key Learning Points**")
            st.write("""
            - Moving Average crossovers excel in clear trending markets
            - They struggle during sideways or highly volatile periods
            - Success depends on proper parameter selection for current market conditions
            - No single strategy works in all market environments
            """)

        elif strategy == "Relative Strength Index - RSI (Momentum)":
            # --- RSI CALCULATION ---
            delta = hist_df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
            rs = gain / loss
            hist_df['RSI'] = 100 - (100 / (1 + rs))
            
            # Generate signals
            hist_df['RSI_Signal'] = 0
            hist_df.loc[hist_df['RSI'] < rsi_oversold, 'RSI_Signal'] = 1  # Oversold - potential buy
            hist_df.loc[hist_df['RSI'] > rsi_overbought, 'RSI_Signal'] = -1  # Overbought - potential sell
            
            hist_df['RSI_Position'] = hist_df['RSI_Signal'].diff()
            buy_signals = hist_df[hist_df['RSI_Position'] == 1]
            sell_signals = hist_df[hist_df['RSI_Position'] == -1]

            # --- RSI VISUALIZATION ---
            st.subheader("RSI Strategy Visualization")
            
            # Create main figure for price
            main_fig = go.Figure()
            
            # Add price data based on chart type
            if hist_chart_type == 'Line':
                main_fig.add_trace(go.Scatter(
                    x=hist_df.index, y=hist_df['Close'], 
                    name='Close Price', line=dict(color='white', width=2)
                ))
            else:
                main_fig.add_trace(go.Candlestick(
                    x=hist_df.index,
                    open=hist_df['Open'], high=hist_df['High'],
                    low=hist_df['Low'], close=hist_df['Close'],
                    name='OHLC'
                ))
            
            # Add buy/sell signals
            main_fig.add_trace(go.Scatter(
                x=buy_signals.index, y=buy_signals['Close'],
                mode='markers', name='Buy Signal',
                marker=dict(color='green', symbol='triangle-up', size=10, line=dict(width=2, color='white'))
            ))
            main_fig.add_trace(go.Scatter(
                x=sell_signals.index, y=sell_signals['Close'],
                mode='markers', name='Sell Signal',
                marker=dict(color='red', symbol='triangle-down', size=10, line=dict(width=2, color='white'))
            ))
            
            main_fig.update_layout(
                title=f"{stock_name} Price with RSI Signals",
                height=400,
                hovermode="x unified",
                margin=dict(l=20, r=20, t=40, b=20)
            )
            main_fig.update_xaxes(rangeslider_visible=False)
            st.plotly_chart(main_fig, use_container_width=True)
            
            # Create separate figure for RSI
            rsi_fig = go.Figure()
            rsi_fig.add_trace(go.Scatter(
                x=hist_df.index, y=hist_df['RSI'],
                name='RSI', line=dict(color='yellow', width=2)
            ))
            
            # Add RSI reference lines
            rsi_fig.add_hline(y=rsi_overbought, line_dash="dash", line_color="red", 
                             annotation_text="Overbought")
            rsi_fig.add_hline(y=rsi_oversold, line_dash="dash", line_color="green", 
                             annotation_text="Oversold")
            rsi_fig.add_hline(y=50, line_dash="dot", line_color="gray")
            
            rsi_fig.update_layout(
                title="RSI Indicator",
                height=300,
                hovermode="x unified",
                margin=dict(l=20, r=20, t=40, b=20),
                yaxis_range=[0, 100]
            )
            st.plotly_chart(rsi_fig, use_container_width=True)

            # --- RSI BACKTEST ---
            cash = investment
            shares = 0
            trades = []
            position = 0  # 0 = no position, 1 = long
            
            for i in range(len(hist_df)):
                current_rsi = hist_df['RSI'].iloc[i]
                current_price = hist_df['Close'].iloc[i]
                
                if position == 0 and current_rsi < rsi_oversold and cash > 0:
                    # Buy signal
                    shares = cash / current_price
                    cash = 0
                    position = 1
                    trades.append({'date': hist_df.index[i], 'action': 'BUY', 'price': current_price, 'rsi': current_rsi})
                
                elif position == 1 and current_rsi > rsi_overbought and shares > 0:
                    # Sell signal
                    cash = shares * current_price
                    shares = 0
                    position = 0
                    trades.append({'date': hist_df.index[i], 'action': 'SELL', 'price': current_price, 'rsi': current_rsi})

            final_value = cash + (shares * hist_df['Close'].iloc[-1])
            profit_percent = ((final_value - investment) / investment) * 100
            
            # Buy & Hold comparison
            buy_hold_value = investment * (hist_df['Close'].iloc[-1] / hist_df['Close'].iloc[0])
            buy_hold_percent = ((buy_hold_value - investment) / investment) * 100

            # --- RSI RESULTS ---
            st.success("RSI Strategy Analysis Completed!")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("RSI Strategy Return", f"{profit_percent:.2f}%", delta=f"{profit_percent:.2f}%")
            col2.metric("Buy & Hold Return", f"{buy_hold_percent:.2f}%", delta=f"{buy_hold_percent:.2f}%")
            col3.metric("Total RSI Trades", len(trades))
            col4.metric("Final Value", f"₹{final_value:,.2f}")

            # --- RSI PERFORMANCE ANALYSIS ---
            st.markdown("---")
            st.subheader("RSI Performance Analysis")

            price_change = ((hist_df['Close'].iloc[-1] - hist_df['Close'].iloc[0]) / hist_df['Close'].iloc[0]) * 100
            rsi_oversold_count = len(hist_df[hist_df['RSI'] < rsi_oversold])
            rsi_overbought_count = len(hist_df[hist_df['RSI'] > rsi_overbought])

            if profit_percent > buy_hold_percent and profit_percent > 0:
                st.success("**RSI Strategy Outperformed**")
                st.write(f"**Performance:** +{profit_percent:.1f}% vs Buy & Hold +{buy_hold_percent:.1f}%")
                
                st.write("""
                **Why it worked:**
                - Effective identification of overbought/oversold conditions
                - Precise timing of market reversals
                - Successful capture of momentum shifts
                - Consistent mean reversion opportunities
                """)

            elif profit_percent > 0:
                st.warning("**RSI Strategy Underperformed**")
                st.write(f"**Performance:** +{profit_percent:.1f}% vs Buy & Hold +{buy_hold_percent:.1f}%")
                
                st.write("""
                **Performance factors:**
                - Strong trending conditions reduced effectiveness
                - Limited extreme RSI readings constrained opportunities
                - Missed portions of sustained directional moves
                - Mixed signal quality across market phases
                """)

            else:
                st.error("**RSI Strategy Resulted in Loss**")
                st.write(f"**Performance:** {profit_percent:.1f}% vs Buy & Hold +{buy_hold_percent:.1f}%")
                
                if rsi_oversold_count == 0 or rsi_overbought_count == 0:
                    st.write("""
                    **Why it struggled:**
                    - Insufficient extreme RSI readings for signals
                    - Indicator remained in neutral territory
                    - Lack of clear overbought/oversold conditions
                    - Market conditions unsuitable for momentum strategies
                    """)
                else:
                    st.write("""
                    **Why it struggled:**
                    - False reversal signals during strong trends
                    - Early entries in continuing trends
                    - Premature exits during momentum moves
                    - High volatility disrupted RSI patterns
                    """)

            # RSI Statistics
            st.markdown("**RSI Signal Analysis**")
            rsi_col1, rsi_col2, rsi_col3 = st.columns(3)
            rsi_col1.metric("Oversold Signals", rsi_oversold_count)
            rsi_col2.metric("Overbought Signals", rsi_overbought_count)
            rsi_col3.metric("Trades Executed", len(trades))

            # Educational Insights
            st.markdown("**Key Learning Points**")
            st.write("""
            - RSI excels in ranging markets with clear oscillations
            - It struggles during strong, sustained trending periods
            - Signal quality depends on proper level calibration
            - Works best when combined with trend confirmation
            """)

        elif strategy == "Bollinger Bands (Volatility)":
            # --- BOLLINGER BANDS CALCULATION ---
            hist_df['BB_Middle'] = hist_df['Close'].rolling(window=bb_period).mean()
            hist_df['BB_Std'] = hist_df['Close'].rolling(window=bb_period).std()
            hist_df['BB_Upper'] = hist_df['BB_Middle'] + (hist_df['BB_Std'] * bb_std)
            hist_df['BB_Lower'] = hist_df['BB_Middle'] - (hist_df['BB_Std'] * bb_std)
            
            # Generate signals - Buy when price touches lower band, Sell when touches upper band
            hist_df['BB_Signal'] = 0
            hist_df.loc[hist_df['Close'] <= hist_df['BB_Lower'], 'BB_Signal'] = 1  # Buy signal
            hist_df.loc[hist_df['Close'] >= hist_df['BB_Upper'], 'BB_Signal'] = -1  # Sell signal
            
            hist_df['BB_Position'] = hist_df['BB_Signal'].diff()
            buy_signals = hist_df[hist_df['BB_Position'] == 1]
            sell_signals = hist_df[hist_df['BB_Position'] == -1]

            # --- BOLLINGER BANDS VISUALIZATION ---
            st.subheader("Bollinger Bands Strategy Visualization")
            
            bb_fig = go.Figure()
            
            if hist_chart_type == 'Line':
                bb_fig.add_trace(go.Scatter(
                    x=hist_df.index, y=hist_df['Close'], 
                    name='Close Price', line=dict(color='white', width=2)
                ))
            else:
                bb_fig.add_trace(go.Candlestick(
                    x=hist_df.index,
                    open=hist_df['Open'], high=hist_df['High'],
                    low=hist_df['Low'], close=hist_df['Close'],
                    name='OHLC'
                ))
            
            # Add Bollinger Bands
            bb_fig.add_trace(go.Scatter(
                x=hist_df.index, y=hist_df['BB_Upper'],
                name='Upper Band', line=dict(color='red', width=1, dash='dash')
            ))
            bb_fig.add_trace(go.Scatter(
                x=hist_df.index, y=hist_df['BB_Middle'],
                name='Middle Band', line=dict(color='yellow', width=1)
            ))
            bb_fig.add_trace(go.Scatter(
                x=hist_df.index, y=hist_df['BB_Lower'],
                name='Lower Band', line=dict(color='green', width=1, dash='dash'),
                fill='tonexty', fillcolor='rgba(0,100,80,0.2)'
            ))
            
            # Add buy/sell signals
            bb_fig.add_trace(go.Scatter(
                x=buy_signals.index, y=buy_signals['Close'],
                mode='markers', name='Buy Signal',
                marker=dict(color='green', symbol='triangle-up', size=10, line=dict(width=2, color='white'))
            ))
            bb_fig.add_trace(go.Scatter(
                x=sell_signals.index, y=sell_signals['Close'],
                mode='markers', name='Sell Signal',
                marker=dict(color='red', symbol='triangle-down', size=10, line=dict(width=2, color='white'))
            ))
            
            bb_fig.update_layout(
                title=f"Bollinger Bands Strategy: {stock_name}",
                height=500,
                hovermode="x unified",
                margin=dict(l=20, r=20, t=40, b=20)
            )
            bb_fig.update_xaxes(rangeslider_visible=False)
            st.plotly_chart(bb_fig, use_container_width=True)

            # --- BOLLINGER BANDS BACKTEST ---
            cash = investment
            shares = 0
            trades = []
            position = 0  # 0 = no position, 1 = long
            
            for i in range(len(hist_df)):
                current_price = hist_df['Close'].iloc[i]
                current_signal = hist_df['BB_Signal'].iloc[i]
                
                if position == 0 and current_signal == 1 and cash > 0:  # Buy signal (touch lower band)
                    shares = cash / current_price
                    cash = 0
                    position = 1
                    trades.append({'date': hist_df.index[i], 'action': 'BUY', 'price': current_price})
                
                elif position == 1 and current_signal == -1 and shares > 0:  # Sell signal (touch upper band)
                    cash = shares * current_price
                    shares = 0
                    position = 0
                    trades.append({'date': hist_df.index[i], 'action': 'SELL', 'price': current_price})

            final_value = cash + (shares * hist_df['Close'].iloc[-1])
            profit_percent = ((final_value - investment) / investment) * 100
            
            # Buy & Hold comparison
            buy_hold_value = investment * (hist_df['Close'].iloc[-1] / hist_df['Close'].iloc[0])
            buy_hold_percent = ((buy_hold_value - investment) / investment) * 100

            # --- BOLLINGER BANDS RESULTS ---
            st.success("Bollinger Bands Strategy Analysis Completed!")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("BB Strategy Return", f"{profit_percent:.2f}%", delta=f"{profit_percent:.2f}%")
            col2.metric("Buy & Hold Return", f"{buy_hold_percent:.2f}%", delta=f"{buy_hold_percent:.2f}%")
            col3.metric("Total BB Trades", len(trades))
            col4.metric("Final Value", f"₹{final_value:,.2f}")

            # --- BOLLINGER BANDS PERFORMANCE ANALYSIS ---
            st.markdown("---")
            st.subheader("Bollinger Bands Performance Analysis")

            price_change = ((hist_df['Close'].iloc[-1] - hist_df['Close'].iloc[0]) / hist_df['Close'].iloc[0]) * 100
            band_touches = len(buy_signals) + len(sell_signals)
            avg_band_width = (hist_df['BB_Upper'] - hist_df['BB_Lower']).mean() / hist_df['BB_Middle'].mean() * 100

            if profit_percent > buy_hold_percent and profit_percent > 0:
                st.success("**Bollinger Bands Strategy Outperformed**")
                st.write(f"**Performance:** +{profit_percent:.1f}% vs Buy & Hold +{buy_hold_percent:.1f}%")
                
                st.write("""
                **Why it worked:**
                - Effective mean reversion principles
                - Precise volatility-based entry points
                - Successful capture of price oscillations
                - Optimal band width for clear signals
                """)

            elif profit_percent > 0:
                st.warning("**Bollinger Bands Strategy Underperformed**")
                st.write(f"**Performance:** +{profit_percent:.1f}% vs Buy & Hold +{buy_hold_percent:.1f}%")
                
                st.write("""
                **Performance factors:**
                - Sustained breakouts reduced effectiveness
                - Band penetration without reversal
                - Missed extended trending movements
                - Suboptimal band width for current volatility
                """)

            else:
                st.error("**Bollinger Bands Strategy Resulted in Loss**")
                st.write(f"**Performance:** {profit_percent:.1f}% vs Buy & Hold +{buy_hold_percent:.1f}%")
                
                if band_touches == 0:
                    st.write("""
                    **Why it struggled:**
                    - Insufficient band interactions for signals
                    - Unusually narrow trading range
                    - Price action confined to middle band
                    - Lack of volatility-based setups
                    """)
                elif avg_band_width > 25:
                    st.write("""
                    **Why it struggled:**
                    - Extreme volatility created false signals
                    - Excessive band width reduced timing precision
                    - Late signal generation during rapid moves
                    - High volatility regime unsuitable for bands
                    """)
                else:
                    st.write("""
                    **Why it struggled:**
                    - Failed mean reversion assumptions
                    - Continuous band breakouts without reversal
                    - Poor timing of volatility entries
                    - Ineffective adaptation to market structure
                    """)

            # Band Analysis
            st.markdown("**Band Behavior Summary**")
            band_col1, band_col2, band_col3 = st.columns(3)
            band_col1.metric("Band Touches", band_touches)
            band_col2.metric("Avg Band Width", f"{avg_band_width:.1f}%")
            band_col3.metric("Trades Executed", len(trades))

            # Educational Insights
            st.markdown("**Key Learning Points**")
            st.write("""
            - Bollinger Bands excel in volatile, ranging markets
            - They struggle during strong breakouts or low volatility
            - Band width should match current market volatility
            - Works exceptionally well with volatile small-cap stocks
            - Often combined with other indicators for confirmation
            """)

# --------------------------------------------------------------------
# SECTION 1 LIVE LOOP (Keep your existing working code)
# --------------------------------------------------------------------
while True:
    try:
        live_info = yf.Ticker(selected_ticker).info
        live_df = yf.Ticker(selected_ticker).history(period="1d", interval="5m")

        with live_placeholder.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Price", f"₹{live_info.get('currentPrice', 0):.2f}",
                          delta=f"{live_info.get('regularMarketChangePercent', 0):.2f}%")
            with col2:
                st.metric("Day High", f"₹{live_info.get('dayHigh', 0):.2f}")
            with col3:
                st.metric("Day Low", f"₹{live_info.get('dayLow', 0):.2f}")

            if not live_df.empty:
                live_fig = px.line(live_df, x=live_df.index, y="Close",
                                   title="Intraday Price Movement (5 min)")
                live_fig.update_layout(height=400, hovermode="x unified",
                                       margin=dict(l=20, r=20, t=40, b=20))
                live_fig.update_xaxes(rangeslider_visible=False)
                st.plotly_chart(live_fig, use_container_width=True,
                                key=f"live_chart_{int(time.time())}")

            st.caption(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")

        time.sleep(20)

    except Exception as e:
        with live_placeholder.container():
            st.error(f"Error fetching live data: {e}")
        time.sleep(20)