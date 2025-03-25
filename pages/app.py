import streamlit as st
from streamlit_option_menu import option_menu
# from config import *

st.logo(
    "static/img/bank_logo.png",
    icon_image="static/img/bank_logo.png")

pages = {
    "Loan Simulations": [
        st.Page(page="simu_loan/basic_loan.py", title="Basic Loan", icon=":material/credit_score:"),
        st.Page(page="simu_loan/advanced_loan.py", title="Advanced Loan", icon=":material/credit_score:"),
        st.Page(page="simu_loan/comparator_loan.py", title="Comparator Loan", icon=":material/credit_score:"),
        st.Page(page="simu_loan/scenario_loan.py", title="Scenario Loan", icon=":material/credit_score:"),
        st.Page(page="simu_loan/vizualize_test.py", title="Vizualize", icon=":material/credit_score:"),
    ],
    "Investment Simulations": [
        st.Page("simu_investment/basic_investment.py", title="Basic Investment", icon=":material/monitoring:"),
    ],
    "Resources": [
        st.Page("resources/contact.py", title="Contact", icon=":material/contacts_product:"),
        st.Page("resources/help.py", title="Need help ?", icon=":material/help:"),
    ],
}

pg = st.navigation(pages)
pg.run()