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
    
    /* MODIFIED: Removed the background color and blur effect */
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
    .stButton > button {{
        background-color: #4ade80;
        color: white;
        font-weight: 900;
        border: none;
    }}
    .stButton > button:hover {{
        background-color: #86efac;
        color: white;
        border: none;
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

col1, col2, col3 = st.columns([1, 1.2, 1])
with col2:
    if st.button("Get Started →", use_container_width=True, type="primary"):
        st.switch_page("pages/Sectors.py")