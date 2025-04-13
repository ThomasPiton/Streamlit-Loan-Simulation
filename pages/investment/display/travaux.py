import streamlit as st
from pages.investment.display.base_section import BaseSection

class Travaux(BaseSection):
    
    def render(self):
        with st.expander("Rénovation, Réparations et Estimations de Travaux", expanded=False):
            st.subheader("Estimations de Rénovation et Travaux")
            active_renovation = st.checkbox("Activer / Désactiver", key=f"active_renovation")
            if active_renovation:
                st.success("**Activée**") 
            else: 
                st.warning("**Désactivée**")
            budget_renovation = st.number_input("Budget de Rénovation Estimé (€)", min_value=0, value=20000, step=1000, key=f"budget_renovation")
            duree_renovation = st.number_input("Durée de Rénovation Estimée (Mois)", min_value=1, value=6, step=1, key=f"duree_renovation")
            type_renovation = st.selectbox("Type de Rénovation",options=["Légère", "Moyenne", "Lourde"],index=0,key=f"type_renovation")