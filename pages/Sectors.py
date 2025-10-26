import streamlit as st
from sector_map import SECTOR_MAP

st.set_page_config(page_title="Explore Sectors", page_icon="🔎", layout="wide", initial_sidebar_state="collapsed")

# Custom styling for titles and cards
st.markdown("""
<style>
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 800;
        text-align: center;
        color: #7c3aed;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.3rem !important;
        text-align: center;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    
    /* Slightly lighter dark blue cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #070F2B;
        border: 1px solid #374151;
        border-radius: 10px;
        padding: 20px;
    }
    
    /* Button styling - same color as cards */
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

# Use custom classes for titles
st.markdown('<div class="main-title">Indian Stock Market</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Explore major sectors and discover investment opportunities.</div>', unsafe_allow_html=True)

st.divider()

cols = st.columns(4)
for i, (sector_name, data) in enumerate(SECTOR_MAP.items()):
    with cols[i % 4]:
        with st.container(border=True):
            st.subheader(f"{data['icon']} {sector_name}")
            st.caption(data['desc'])
            if st.button("Explore →", key=f"explore_{sector_name}", use_container_width=True):
                st.session_state.selected_sector = sector_name
                st.switch_page("pages/Companies.py")