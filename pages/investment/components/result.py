import streamlit as st
from pages.investment.components.base_section import BaseSection
from pages.investment.computation.investment_model import InvestmentModel
from pages.investment.displayer.display_factory import DisplayFactory

class Result(BaseSection):
    
    def render(self):
        
        st.header("Résumé du projet")
        model = InvestmentModel()
        success = model.run()
        
        if not success:
            st.error("Impossible de calculer les résultats en raison d'erreurs dans les données fournies.")
            return
            
        # resultats = model.get_resultats()
        st.subheader("Résultat du Bien")
        tabs = st.tabs(["Bien1", "Bien2", "Bien3"])
        with tabs[0]:
            DisplayFactory(display="DISPLAY_RESULT_BIEN").render()
        with tabs[1]:
            pass
        with tabs[2]:
            pass
        
        st.subheader("Résultat du Loyer")
        tabs = st.tabs(["Loyer1", "Loyer2", "Loyer3"])
        with tabs[0]:
            pass
        with tabs[1]:
            pass
        with tabs[2]:
            pass
        
        st.subheader("Résultat du Prêt")
        tabs = st.tabs(["Pret1", "Pret2", "Pret3"])
        with tabs[0]:
            pass
        with tabs[1]:
            pass
        with tabs[2]:
            pass
        
        
