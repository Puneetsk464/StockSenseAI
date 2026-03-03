import streamlit as st
import pandas as pd
from sector_map import SECTOR_MAP

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Companies by Sector",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CSS (unchanged)
# --------------------------------------------------
st.markdown("""
<style>
    .sector-title {
        font-size: 3.5rem !important;
        font-weight: 800;
        color: #7c3aed;
        margin-bottom: 1rem;
    }

    .sector-subtitle {
        font-size: 1.4rem !important;
        color: #6b7280;
        margin-bottom: 2rem;
    }

    [data-baseweb="tab"] {
        font-size: 1.2rem;
        padding: 10px 0px !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #070F2B;
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 20px;
    }

    .stButton > button {
        background-color: #070F2B;
        color: white;
        border: 1px solid #374151;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #059669 !important;
        color: white !important;
        border: none !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Back button
# --------------------------------------------------
if st.button("← Back to Sectors", key="back_button"):
    st.switch_page("pages/Sectors.py")

st.divider()

# --------------------------------------------------
# Load data
# --------------------------------------------------
try:
    df = pd.read_csv("stock_data.csv")
    selected_sector = st.session_state.get("selected_sector")
except FileNotFoundError:
    st.error("Data file 'stock_data.csv' not found. Please run fetch_data.py first.")
    st.stop()

if not selected_sector:
    st.error("No sector selected. Please return to the Sectors page.")
    st.stop()

sector_info = SECTOR_MAP.get(selected_sector, {"icon": "📊"})

st.markdown(
    f'<div class="sector-title">{sector_info["icon"]} {selected_sector} Sector</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="sector-subtitle">Companies categorized by Market Capitalization.</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# Filter by sector and cap
# --------------------------------------------------
sector_df = df[df["Sector"] == selected_sector]

large = sector_df[sector_df["MarketCapCategory"] == "Large Cap"]
mid = sector_df[sector_df["MarketCapCategory"] == "Mid Cap"]
small = sector_df[sector_df["MarketCapCategory"] == "Small Cap"]

tabL, tabM, tabS = st.tabs([
    f"Large Cap ({len(large)})",
    f"Mid Cap ({len(mid)})",
    f"Small Cap ({len(small)})"
])

# --------------------------------------------------
# Card renderer (UNCHANGED)
# --------------------------------------------------
def render_company_cards(df_subset, key_prefix):
    for row in df_subset.itertuples():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(row.Name)
                st.caption(row.Symbol)
            with col2:
                st.write("")
                if st.button(
                    "View →",
                    key=f"{key_prefix}_{row.Symbol}",
                    use_container_width=True
                ):
                    st.session_state.selected_ticker = row.Symbol
                    st.switch_page("pages/Stock_Details.py")

# --------------------------------------------------
# Two-column layout per cap
# --------------------------------------------------
def show_cap_layout(df_subset, cap_name):
    if df_subset.empty:
        st.info(f"No {cap_name} companies found.")
        return

    # Top 5 on the left
    top_5 = df_subset.head(5)

    # Remaining on the right
    remaining = df_subset.iloc[5:]

    left_col, right_col = st.columns([2, 1])

    # LEFT: Top Performing Stocks
    with left_col:
        st.subheader("Top Performing Stocks")
        render_company_cards(top_5, f"{cap_name}_TOP")

    # RIGHT: Remaining Stocks (scrollable)
    with right_col:
        st.subheader("All Stocks")
        if remaining.empty:
            st.caption("No additional stocks available.")
        else:
            with st.container(height=520):
                render_company_cards(remaining, f"{cap_name}_ALL")

# --------------------------------------------------
# Tabs
# --------------------------------------------------
with tabL:
    show_cap_layout(large, "Large Cap")

with tabM:
    show_cap_layout(mid, "Mid Cap")

with tabS:
    show_cap_layout(small, "Small Cap")
