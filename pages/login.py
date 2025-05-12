import streamlit as st

USERNAME = "admin"
PASSWORD = "1234"

st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

col1, col2 = st.columns(2)

with col1:
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.switch_page("pages/about.py")
        else:
            st.error("Incorrect credentials")

with col2:
    if st.button("Continue as Guest"):
        st.warning("You are continuing without login.")
        st.switch_page("pages/01_simu_basic.py")  # Send guest to basic simulation
