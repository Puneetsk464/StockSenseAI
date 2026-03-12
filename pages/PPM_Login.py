import streamlit as st
from firebase_config import auth, db

st.set_page_config(
    page_title="PPM Login",
    page_icon="📊",
    layout="centered"
)

# ------------------- BACK BUTTON -------------------

if st.button("← Back to Home"):
    st.switch_page("Home.py")

st.title("Personal Portfolio Manager")

st.write("Login or create an account to continue.")

st.divider()

# ------------------- LOGIN SECTION -------------------

st.subheader("Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login", use_container_width=True):

    if email == "" or password == "":
        st.warning("Please enter email and password.")

    else:
        try:
            user = auth.sign_in_with_email_and_password(email, password)

            user_id = user["localId"]

            st.session_state.user_id = user_id
            st.session_state.user_email = email

            # Check if profile exists
            doc = db.collection("users").document(user_id).get()

            if doc.exists:
                st.success("Login successful")
                st.switch_page("pages/PPM_Dashboard.py")

            else:
                st.success("Please complete your profile")
                st.switch_page("pages/PPM_Profile.py")

        except Exception as e:
            st.error("Login failed")
            st.write(e)


st.divider()

# ------------------- SIGNUP SECTION -------------------

st.subheader("Create Account")

if st.button("Sign Up", use_container_width=True):

    if email == "" or password == "":
        st.warning("Please enter email and password.")

    else:
        try:
            user = auth.create_user_with_email_and_password(email, password)

            user_id = user["localId"]

            st.session_state.user_id = user_id
            st.session_state.user_email = email

            st.success("Account created successfully")

            st.switch_page("pages/PPM_Profile.py")

        except Exception as e:
            st.error("Signup failed")
            st.write(e)