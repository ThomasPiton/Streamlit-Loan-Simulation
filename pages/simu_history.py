import streamlit as st
import pandas as pd

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("You must be logged in to view your simulation history.")
    st.stop()

st.title("Simulation History")

# Dummy example data
data = pd.DataFrame({
    "Date": ["2025-05-10", "2025-05-09"],
    "Type": ["Loan", "Savings"],
    "Result": ["Approved", "Projected: €12,400"]
})

st.dataframe(data)

if st.button("Download History as CSV"):
    st.download_button("Download", data.to_csv(index=False), file_name="history.csv")
