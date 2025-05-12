import streamlit as st

# --- Access Control ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("You must be logged in to access your settings.")
    st.stop()

# --- Simulated user data (in real use, you'd fetch this from a DB or user state) ---
user_profile = {
    "username": "admin",
    "full_name": "Admin User",
    "email": "admin@bankapp.com",
    "join_date": "2024-01-15",
    "preferred_currency": "EUR",
    "language": "English"
}

st.title("👤 Profile & Settings")

# --- Profile Section ---
st.subheader("User Profile")

col1, col2 = st.columns(2)
with col1:
    st.text_input("Full Name", user_profile["full_name"], disabled=True)
    st.text_input("Username", user_profile["username"], disabled=True)

with col2:
    st.text_input("Email", user_profile["email"], disabled=True)
    st.text_input("Member Since", user_profile["join_date"], disabled=True)

st.divider()

# --- Preferences Section ---
st.subheader("Preferences")

currency = st.selectbox("Preferred Currency", ["EUR", "USD", "GBP", "CHF"], index=0)
language = st.selectbox("Language", ["English", "Français", "Deutsch"], index=0)

if st.button("Save Preferences"):
    # In a real app, save these settings to a database or file
    st.success("Preferences saved!")

st.divider()

# --- Security Section ---
st.subheader("Security Settings")

st.info("Password change feature coming soon.")

if st.button("Log Out"):
    st.session_state.clear()
    st.rerun()
