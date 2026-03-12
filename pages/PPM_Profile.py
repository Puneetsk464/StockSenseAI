import streamlit as st
from firebase_config import db
from datetime import datetime

st.set_page_config(
    page_title="Complete Your Profile",
    page_icon="📊",
    layout="centered"
)

st.title("Investor Profile Setup")

st.write("Please provide your financial details to personalize your portfolio recommendations.")

st.divider()

# Check if user is logged in
if "user_id" not in st.session_state:
    st.error("You must login first.")
    st.stop()

user_id = st.session_state.user_id

# ------------------- FORM -------------------

age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    step=1
)

income = st.number_input(
    "Annual Income (₹)",
    min_value=0.0,
    step=50000.0,
    help="Example: 800000 = ₹8 lakh"
)

corpus = st.number_input(
    "Current Investment Corpus (₹)",
    min_value=0.0,
    step=10000.0,
    help="Example: 200000 = ₹2 lakh"
)

horizon = st.number_input(
    "Investment Horizon (Months)",
    min_value=3,
    max_value=120,
    step=1,
    help="Example: 12 = 1 year, 36 = 3 years"
)

risk_appetite = st.slider(
    "Risk Appetite (1 = Very Conservative, 5 = Very Aggressive)",
    min_value=1,
    max_value=5,
    value=3
)

investment_goal = st.text_input(
    "Investment Goal (e.g., Retirement, Wealth Growth, Buying a House)"
)

st.divider()

# ------------------- SAVE BUTTON -------------------

if st.button("Save Profile", use_container_width=True):

    profile_data = {
        "age": age,
        "income": income,
        "corpus": corpus,
        "horizon_months": horizon,
        "risk_appetite": risk_appetite,
        "investment_goal": investment_goal,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    try:
        db.collection("users").document(user_id).set(profile_data)

        st.success("Profile saved successfully!")

        st.switch_page("pages/PPM_Dashboard.py")

    except Exception as e:
        st.error("Failed to save profile.")
        st.write(e)