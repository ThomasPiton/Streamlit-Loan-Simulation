import streamlit as st

st.write("Advanced Loan")

col1, col2, col3, col4 = st.columns(4)
    
with col1:
    param1 = st.text_input("montant")
    param2 = st.text_input("Parameter 2")

with col2:
    param3 = st.text_input("Parameter 3")
    param4 = st.text_input("Parameter 4")
    
with col3:
    param5 = st.text_input("Parameter 5")
    param6 = st.text_input("Parameter 6")
    
with col4:
    param7 = st.text_input("Parameter 7")
    param8 = st.text_input("Parameter 8")