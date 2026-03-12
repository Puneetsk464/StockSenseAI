import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Welcome to StockSense AI",
    page_icon="🤖",
    layout="centered"
)

# --- Function to read an image file and convert it to Base64 ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- Function to set the background and apply styles ---
def set_page_style(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_style = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    #MainMenu {{visibility: hidden;}}
    [data-testid="stSidebar"] {{display: none;}}
    footer {{visibility: hidden;}}

    .title-container {{
        text-align: center;
        padding: 2rem 0 0 0;
    }}

    .title-container h1 {{
        font-size: 3.5rem;
    }}

    h2 {{
        text-align: center;
    }}

    /* Premium Institutional Button Style */
    .stButton > button {{
        background-color: #0f172a;     
        color: #f8fafc;
        font-weight: 800;
        border: 2px solid #facc15;     
        border-radius: 12px;
        height: 85px;                  
        font-size: 1.15rem;            
        letter-spacing: 0.6px;
        padding: 0 28px;               
    }}

    .stButton > button:hover {{
        background-color: #1e293b;     
        border: 2px solid #fde047;     
        color: white;
    }}

    .or-text {{
        text-align: center;
        font-weight: 900;
        font-size: 1.25rem;
        color: #facc15;
        margin-top: 30px;
    }}
    </style>
    """
    st.markdown(page_style, unsafe_allow_html=True)

# --- Use the function to set your background ---
if os.path.exists("assets/background.png"):
    set_page_style("assets/background.png")
else:
    st.warning("Background image not found. Please add it to the 'assets' folder.")

# --- Page Content ---
st.markdown(
    """
    <div class="title-container">
        <h1>StockSense AI 🤖</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.header("Your Personal Investment Strategist")
st.write("")
st.divider()

# -------------------- BUTTONS --------------------
col1, col_or, col2 = st.columns([1.4, 0.3, 1.4])

with col1:
    if st.button("LEARN STOCK MARKET STRATEGIES →", use_container_width=True):
        st.switch_page("pages/Sectors.py")

with col_or:
    st.markdown('<div class="or-text">OR</div>', unsafe_allow_html=True)

with col2:
    if st.button("SMART PERSONAL PORTFOLIO MANAGEMENT →", use_container_width=True):
        st.switch_page("pages/PPM_Login.py")