import streamlit as st
from models.advanced_simulation.component.base_section import BaseSection
from models.advanced_simulation.computation.investment_model import InvestmentModel
from models.advanced_simulation.displayer.display_factory import DisplayFactory

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
            DisplayFactory(display="DISPLAY_RESULT_V1").render()
        with tabs[1]:
            DisplayFactory(display="DISPLAY_RESULT_V2").render()
            DisplayFactory(display="DISPLAY_RESULT_V3").render()
        with tabs[2]:
            DisplayFactory(display="DISPLAY_RESULT_V4").render()
            DisplayFactory(display="DISPLAY_RESULT_V5").render()
        
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
        
        
