import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from firebase_config import db

from ppm.risk_model import predict_risk, risk_category
from ppm.portfolio_optimizer import build_portfolio


# -------- PROJECTION CALCULATION --------

def calculate_portfolio_projections(corpus, annual_return, volatility, horizon_months):
    """
    Calculate portfolio projections based on user's actual investment horizon.

    Adapts granularity based on horizon:
    - < 6 months: Monthly projections
    - 6-24 months: Quarterly projections
    - > 24 months: Annual projections

    Uses compound growth formula:
    Future Value = Corpus * (1 + period_return)^periods
    """

    # Determine time period and granularity
    if horizon_months < 6:
        # Monthly breakdown for short-term
        periods = horizon_months
        period_label = "Month"
        period_return = annual_return / 12  # Approximate monthly

    elif horizon_months < 24:
        # Quarterly breakdown for medium-term
        periods = horizon_months // 3
        period_label = "Quarter"
        period_return = annual_return / 4  # Approximate quarterly

    else:
        # Annual breakdown for long-term
        periods = horizon_months // 12
        period_label = "Year"
        period_return = annual_return  # Annual

    periods_array = np.arange(0, int(periods) + 1)

    # Volatility scaled to matching period
    if period_label == "Month":
        period_volatility = volatility / np.sqrt(12)
    elif period_label == "Quarter":
        period_volatility = volatility / np.sqrt(4)
    else:
        period_volatility = volatility

    # Realistic scenario (expected return)
    realistic = corpus * (1 + period_return) ** periods_array

    # Optimistic scenario (return + volatility)
    optimistic = corpus * (1 + period_return +
                           period_volatility) ** periods_array

    # Conservative scenario (return - volatility, minimum 0)
    conservative_rate = max(0, period_return - period_volatility)
    conservative = corpus * (1 + conservative_rate) ** periods_array

    return {
        "periods": periods_array,
        "period_label": period_label,
        "realistic": realistic,
        "optimistic": optimistic,
        "conservative": conservative,
        "horizon_months": horizon_months
    }


st.set_page_config(
    page_title="PPM Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- SESSION PROTECTION ----------------

if "user_id" not in st.session_state:
    st.warning("Please login first.")
    st.switch_page("pages/PPM_Login.py")

user_id = st.session_state.user_id


# ---------------- FETCH USER DATA ----------------

doc = db.collection("users").document(user_id).get()

if not doc.exists:
    st.error("Profile not found.")
    st.switch_page("pages/PPM_Profile.py")

user_data = doc.to_dict()


# ---------------- PAGE HEADER ----------------

st.title("Personal Portfolio Dashboard")

st.write(f"Welcome **{st.session_state.user_email}**")

st.divider()


# ---------------- PROFILE DISPLAY ----------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Age", user_data["age"])

with col2:
    st.metric("Annual Income", f"₹{int(user_data['income']):,}")

with col3:
    st.metric("Investment Corpus", f"₹{int(user_data['corpus']):,}")


col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Investment Horizon", f"{user_data['horizon_months']} months")

with col5:
    st.metric("Risk Appetite", user_data["risk_appetite"])

with col6:
    st.metric("Investment Goal", user_data["investment_goal"])

st.divider()


# ---------------- ACTION BUTTONS ----------------

colA, colB, colC = st.columns(3)

with colA:
    if st.button("Edit Profile", use_container_width=True):
        st.switch_page("pages/PPM_Profile.py")

with colB:
    if st.button("Refresh Data", use_container_width=True):
        st.rerun()

with colC:
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/PPM_Login.py")

st.divider()


# ---------------- ML RISK MODEL ----------------

st.subheader("Risk Assessment")

risk_score = predict_risk(
    user_data["age"],
    user_data["income"],
    user_data["corpus"],
    user_data["horizon_months"],
    user_data["risk_appetite"]
)

risk_cat = risk_category(risk_score)

colR1, colR2 = st.columns(2)

with colR1:
    st.metric("Risk Score", f"{risk_score:.2f}")

with colR2:
    st.metric("Risk Category", risk_cat)

st.divider()


# ---------------- PORTFOLIO ENGINE ----------------

st.subheader("Portfolio Recommendation Engine")

with st.spinner("Generating optimized portfolio..."):

    portfolio = build_portfolio(risk_cat)

if portfolio.empty:
    st.warning("Portfolio could not be generated.")
else:

    # ---------------- TABLE ----------------

    st.write("### Recommended Stocks")

    st.dataframe(
        portfolio[[
            "symbol",
            "sector",
            "market_cap",
            "predicted_return",
            "volatility",
            "weight"
        ]],
        use_container_width=True
    )

    st.divider()

    # ---------------- STOCK PIE CHART ----------------

    colP1, colP2 = st.columns(2)

    with colP1:

        fig = px.pie(
            portfolio,
            values="weight",
            names="symbol",
            title="Recommended Stock Allocation"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ---------------- ASSET ALLOCATION ----------------

    with colP2:

        if risk_cat == "Conservative":

            allocation = {
                "Stocks": 40,
                "Mutual Funds": 30,
                "Gold": 15,
                "FD": 15
            }

        elif risk_cat == "Moderate":

            allocation = {
                "Stocks": 60,
                "Mutual Funds": 20,
                "Gold": 10,
                "FD": 10
            }

        else:

            allocation = {
                "Stocks": 80,
                "Mutual Funds": 10,
                "Gold": 5,
                "FD": 5
            }

        alloc_df = pd.DataFrame(
            allocation.items(),
            columns=["Asset", "Allocation"]
        )

        fig2 = px.pie(
            alloc_df,
            values="Allocation",
            names="Asset",
            title="Recommended Asset Allocation"
        )

        st.plotly_chart(fig2, use_container_width=True)

st.divider()


# -------- PORTFOLIO PROJECTIONS --------

st.subheader("Investment Growth Projections")

if not portfolio.empty:

    # Calculate portfolio metrics
    portfolio_annual_return = (
        portfolio["predicted_return"] * portfolio["weight"]).sum()
    portfolio_volatility = (
        portfolio["volatility"] * portfolio["weight"]).sum()

    st.write(f"""
    **Portfolio Summary:**
    - Expected Annual Return: **{portfolio_annual_return*100:.2f}%**
    - Portfolio Volatility: **{portfolio_volatility*100:.2f}%**
    - Investment Horizon: **{user_data['horizon_months']} months ({user_data['horizon_months']/12:.1f} years)**
    - Starting Corpus: **₹{int(user_data['corpus']):,}**
    """)

    st.divider()

    # Calculate projections based on actual horizon
    projections = calculate_portfolio_projections(
        corpus=user_data['corpus'],
        annual_return=portfolio_annual_return,
        volatility=portfolio_volatility,
        horizon_months=user_data['horizon_months']
    )

    # Create projection dataframe
    period_label = projections["period_label"]
    projection_df = pd.DataFrame({
        period_label: projections["periods"],
        "Conservative": projections["conservative"],
        "Realistic": projections["realistic"],
        "Optimistic": projections["optimistic"]
    })

    # Create line chart
    fig_projection = go.Figure()

    fig_projection.add_trace(go.Scatter(
        x=projection_df[period_label],
        y=projection_df["Conservative"],
        mode='lines',
        name='Conservative',
        line=dict(color='#FF6B6B', dash='dash'),
        fill=None
    ))

    fig_projection.add_trace(go.Scatter(
        x=projection_df[period_label],
        y=projection_df["Realistic"],
        mode='lines+markers',
        name='Realistic',
        line=dict(color='#4ECDC4', width=3),
        fill='tozeroy',
        fillcolor='rgba(78, 205, 196, 0.2)'
    ))

    fig_projection.add_trace(go.Scatter(
        x=projection_df[period_label],
        y=projection_df["Optimistic"],
        mode='lines',
        name='Optimistic',
        line=dict(color='#95E1D3', dash='dot'),
        fill=None
    ))

    fig_projection.update_layout(
        title=f"Portfolio Value Projections ({period_label.lower()} by {period_label.lower()})",
        xaxis_title=period_label,
        yaxis_title="Portfolio Value (₹)",
        hovermode='x unified',
        height=500,
        template='plotly_white',
        yaxis=dict(
            tickformat='₹,.0f'
        )
    )

    st.plotly_chart(fig_projection, use_container_width=True)

    st.divider()

    # Display projection table
    st.write("### Projection Details")

    display_df = projection_df.copy()
    display_df["Conservative"] = display_df["Conservative"].apply(
        lambda x: f"₹{int(x):,}")
    display_df["Realistic"] = display_df["Realistic"].apply(
        lambda x: f"₹{int(x):,}")
    display_df["Optimistic"] = display_df["Optimistic"].apply(
        lambda x: f"₹{int(x):,}")
    display_df[period_label] = display_df[period_label].astype(int)

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.divider()

    # Key metrics
    col_metrics_1, col_metrics_2, col_metrics_3 = st.columns(3)

    final_realistic = projections["realistic"][-1]
    final_optimistic = projections["optimistic"][-1]
    final_conservative = projections["conservative"][-1]

    with col_metrics_1:
        gains = final_realistic - user_data['corpus']
        gain_pct = (gains / user_data['corpus']) * 100
        st.metric(
            "Realistic Final Value",
            f"₹{int(final_realistic):,}",
            f"+₹{int(gains):,} ({gain_pct:.1f}%)"
        )

    with col_metrics_2:
        gains_opt = final_optimistic - user_data['corpus']
        gain_pct_opt = (gains_opt / user_data['corpus']) * 100
        st.metric(
            "Optimistic Final Value",
            f"₹{int(final_optimistic):,}",
            f"+₹{int(gains_opt):,} ({gain_pct_opt:.1f}%)"
        )

    with col_metrics_3:
        gains_cons = final_conservative - user_data['corpus']
        gain_pct_cons = (
            gains_cons / user_data['corpus']) * 100 if user_data['corpus'] > 0 else 0
        st.metric(
            "Conservative Final Value",
            f"₹{int(final_conservative):,}",
            f"+₹{int(gains_cons):,} ({gain_pct_cons:.1f}%)"
        )

else:
    st.warning("Cannot calculate projections without a portfolio.")
