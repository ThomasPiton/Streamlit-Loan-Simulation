import streamlit as st
from streamlit_option_menu import option_menu
# from config import *

st.logo(
    "static/img/bank_logo.png",
    icon_image="static/img/bank_logo.png")

pages = {
    "Simulations": [
        st.Page(page="basic_loan.py", title="Basic Loan", icon=":material/monitoring:"),
        st.Page(page="advanced_loan.py", title="Advanced Loan", icon=":material/monitoring:"),
        st.Page(page="comparator_loan.py", title="Comparator Loan", icon=":material/monitoring:"),
        st.Page(page="scenario_loan.py", title="Scenario Loan", icon=":material/monitoring:"),
    ],
    "Resources": [
        st.Page("contact.py", title="Contact", icon=":material/contacts_product:"),
        st.Page("help.py", title="Need help ?", icon=":material/help:"),
    ],
}

pg = st.navigation(pages)
pg.run()