import streamlit as st
from pages.investment.components.base_section import BaseSection
from pages.investment.components.data_store import DataStore
from pages.investment.computation import InvestmentModel
class Result(BaseSection):
    
    def render(self):
        st.header("Résultats Finaux")
        model = InvestmentModel()
        model.run()
        
        data = DataStore.all()
        st.write("### Résumé des paramètres saisis :")
        for section, params in data.items():
            st.subheader(section.capitalize())
            st.json(params)