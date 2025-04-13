import streamlit as st
from pages.investment.display.base_section import BaseSection
from data_store import DataStore

class Charges(BaseSection):
    
    def render(self):
        with st.expander("Dépenses Courantes et Charges Récurrentes", expanded=False):
            st.subheader("Dépenses et Charges Récurrentes")
            active_charges = st.checkbox("Activer / Désactiver", key=f"active_charges")
            if active_charges:
                st.success("**Activée**") 
            else: 
                st.warning("**Désactivée**")
            taxe_fonciere = st.number_input("Taxe Foncière Annuelle (€)", min_value=0, value=1500, step=100, key=f"taxe_fonciere")
            frais_assurance = st.number_input("Frais d'Assurance (€)", min_value=0, value=500, step=50, key=f"frais_assurance")
            frais_gestion = st.number_input("Frais de Gestion (%)", min_value=0.0, max_value=10.0, value=5.0, step=0.1, key=f"frais_gestion")
            frais_entretien = st.number_input("Budget d'Entretien et Réparations (€)", min_value=0, value=1000, step=100, key=f"frais_entretien")
            
            # stocke les paramètres
            DataStore.set("charges", {
                "active": active_charges,
                "taxe_fonciere": taxe_fonciere,
                "frais_assurance": frais_assurance,
                "frais_gestion": frais_gestion,
                "frais_entretien": frais_entretien
            })