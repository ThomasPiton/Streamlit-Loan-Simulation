import streamlit as st

st.title("Logout")

# Check if the user is actually logged in
if "logged_in" in st.session_state and st.session_state.logged_in:
    if st.button("Logout"):
        # Clear session and redirect
        st.session_state.clear()
        st.success("You have been logged out.")
        st.rerun()  # Refresh after logout
        # Optional: redirect to login page after a brief pause
        # st.switch_page("pages/login.py") ← uncomment if you're using multipage routing
else:
    st.info("You are not logged in.")
    if st.button("Go to login"):
        st.switch_page("pages/login.py")