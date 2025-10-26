import streamlit as st
import pandas as pd
from sector_map import SECTOR_MAP

st.set_page_config(page_title="Companies by Sector", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

# --- CSS to make Title and Tabs bigger ---
st.markdown("""
<style>
    /* Sector title with purple color (not gradient) */
    .sector-title {
        font-size: 3.5rem !important;
        font-weight: 800;
        color: #7c3aed;
        margin-bottom: 1rem;
    }
    
    /* Sector subtitle bigger */
    .sector-subtitle {
        font-size: 1.4rem !important;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    
    /* Increase the font size of the tab labels */
    [data-baseweb="tab"] {
        font-size: 1.2rem;
        padding: 10px 0px !important;
    }
    
    /* Company cards - same color scheme as Sectors page */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #070F2B;
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 20px;
    }
    
    /* View buttons - same color scheme as Sectors page */
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
    
    /* Back button - red hover only */
    .stButton > button:has(+ .back-button) {
        background-color: #070F2B !important;
        color: white !important;
        border: 1px solid #374151 !important;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:has(+ .back-button):hover {
        background-color: #dc2626 !important;
        color: white !important;
        border: none !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }
</style>
""", unsafe_allow_html=True)


if st.button("← Back to Sectors", key="back_button"):
    st.switch_page("pages/Sectors.py")

st.divider()

try:
    df = pd.read_csv("stock_data.csv")
    selected_sector = st.session_state.get("selected_sector")
except FileNotFoundError:
    st.error("Data file 'stock_data.csv' not found. Please run `fetch_data.py` first.")
    st.stop()

if not selected_sector:
    st.error("No sector selected. Please return to the Sectors page and choose one.")
    st.stop()

sector_info = SECTOR_MAP.get(selected_sector, {"icon": "📊"})
st.markdown(f'<div class="sector-title">{sector_info["icon"]} <span style="color: #7c3aed">{selected_sector} Sector</span></div>', unsafe_allow_html=True)
st.markdown('<div class="sector-subtitle">Companies categorized by Market Capitalization.</div>', unsafe_allow_html=True)

sector_df = df[df["Sector"] == selected_sector]

large = sector_df[sector_df["MarketCapCategory"] == "Large Cap"]
mid = sector_df[sector_df["MarketCapCategory"] == "Mid Cap"]
small = sector_df[sector_df["MarketCapCategory"] == "Small Cap"]

tabL, tabM, tabS = st.tabs([f"Large Cap ({len(large)})", f"Mid Cap ({len(mid)})", f"Small Cap ({len(small)})"])

# --- UI MODIFICATION: This function now creates a full-width, single-column list ---
def show_companies(df_subset, cap_name):
    """Creates a card-like layout for each company."""
    if df_subset.empty:
        st.info(f"No {cap_name} companies found for this sector in our list.")
        return

    # The column grid has been removed to list items vertically at full width
    for row in df_subset.itertuples():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(row.Name)
                st.caption(row.Symbol)
            with col2:
                st.write("") # Vertical spacer for alignment
                if st.button("View →", key=f"{cap_name}_{row.Symbol}", use_container_width=True):
                    st.session_state.selected_ticker = row.Symbol
                    st.switch_page("pages/Stock_Details.py")
# --- END OF UI MODIFICATION ---


with tabL:
    show_companies(large, "Large Cap")
with tabM:
    show_companies(mid, "Mid Cap")
with tabS:
    show_companies(small, "Small Cap")