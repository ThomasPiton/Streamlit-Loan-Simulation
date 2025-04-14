import streamlit as st
from pages.investment.components.base_section import BaseSection
from pages.investment.components.data_store import DataStore

class Result(BaseSection):
    
    def render(self):
        st.header("Résultats Finaux")
        data = DataStore.all()

        st.write("### Résumé des paramètres saisis :")
        for section, params in data.items():
            st.subheader(section.capitalize())
            st.json(params)