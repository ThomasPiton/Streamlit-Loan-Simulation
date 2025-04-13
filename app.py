import streamlit as st
from streamlit_option_menu import option_menu
# from config import *

st.logo(
    "static/img/bank_logo.png",
    icon_image="static/img/bank_logo.png")

pages = {
    "Loan Simulations": [
        st.Page(page="pages/simu_loan/full_investment_analysis.py", title="Full Investment Analysis", icon=":material/credit_score:"),
        st.Page(page="pages/simu_loan/basic_loan.py", title="Basic Loan", icon=":material/credit_score:"),
        st.Page(page="pages/simu_loan/comparator_loan.py", title="Comparator Loan", icon=":material/credit_score:"),
        st.Page(page="pages/simu_loan/scenario_loan.py", title="Scenario Loan", icon=":material/credit_score:"),
        st.Page(page="pages/simu_loan/structured_loan.py", title="Structured Loan", icon=":material/credit_score:"),
        st.Page(page="pages/simu_loan/vizualize_test.py", title="Vizualize", icon=":material/credit_score:"),
    ],
    "Investment Simulations": [
        st.Page("pages/investment/full_investment_analysis2.py", title="Full Investment Analysis 2", icon=":material/monitoring:"),
    ],
    "Resources": [
        st.Page("pages/others/contact.py", title="Contact", icon=":material/contacts_product:"),
        st.Page("pages/others/help.py", title="Need help ?", icon=":material/help:"),
    ],
}

pg = st.navigation(pages)
pg.run()