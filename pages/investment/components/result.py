import streamlit as st
from pages.investment.components.base_section import BaseSection
from pages.investment.computation.investment_model import InvestmentModel

class Result(BaseSection):
    
    def render(self):
        st.header("Résultats Finaux")
        model = InvestmentModel()
        success = model.run()
        
        if not success:
            st.error("Impossible de calculer les résultats en raison d'erreurs dans les données fournies.")
            return
            
        resultats = model.get_resultats()
        
