import streamlit as st
from pages.investment.display.base_section import BaseSection

class FraisAchat(BaseSection):
    
    def render(self):
        with st.expander("Coûts d'Acquisition et Frais", expanded=False):
            st.subheader(f"Coûts d'Acquisition et Frais")
            active_cost = st.checkbox("Activer / Désactiver", key=f"active_cost")
            if active_cost:
                st.success("**Activée**") 
            else: 
                st.warning("**Désactivée**")
            cout_acquisition = st.number_input("Coût d'Acquisition (€)", min_value=0, value=5000, step=100, key=f"cout_acquisition")
            frais_notaire = st.number_input("Frais de Notaire (%)", min_value=0.0, max_value=10.0, value=7.0, step=0.1, key=f"frais_notaire")
            droits_mutation = st.number_input("Droits de Mutation (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1, key=f"droits_mutation")
            autres_frais = st.number_input("Autres Frais d'Acquisition (€)", min_value=0, value=1000, step=100, key=f"autres_frais")