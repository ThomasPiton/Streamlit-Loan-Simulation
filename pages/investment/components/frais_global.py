import streamlit as st
from pages.investment.components.base_section import BaseSection
from pages.investment.components.data_store import DataStore

class FraisGlobal(BaseSection):
    
    def render(self):
        with st.expander("Frais Globaux du Projet", expanded=False):
            st.subheader("Frais Globaux du Projet")

            active = st.checkbox("Activer / Désactiver", key="frais_global_active")
            if active:
                st.success("**Section Activée**") 
            else: 
                st.warning("**Section Désactivée**")

            # --- FRAIS D'ACQUISITION ---
            st.markdown("### Frais d'Acquisition")
            frais_notaire = st.number_input("Frais de Notaire (%)", min_value=0.0, max_value=10.0, value=7.0, step=0.1, key="frais_notaire")
            frais_agence_immo = st.number_input("Frais d'Agence Immobilière (%)", min_value=0.0, max_value=10.0, value=5.0, step=0.1, key="frais_agence_immo")

            # --- FRAIS FINANCIERS GLOBAUX ---
            st.markdown("### Frais Financiers Généraux")
            frais_courtage = st.number_input("Frais de Courtage (en €)", min_value=0.0, value=1000.0, step=100.0, key="frais_courtage")

            # --- FRAIS ANNEXES / OPÉRATIONNELS ---
            st.markdown("### Frais Annexes")
            frais_syndic = st.number_input("Frais de Règlement de Copropriété (en €)", min_value=0.0, value=0.0, step=50.0, key="frais_syndic")
            frais_divers = st.number_input("Autres Frais Divers (en €)", min_value=0.0, value=0.0, step=100.0, key="frais_divers")
            provision_charges = st.number_input("Provision Charges de Copropriété (en €)", min_value=0.0, value=0.0, step=100.0, key="provision_charges")

            # Stockage
            if active:
                DataStore.set("frais_global", {
                    "active": active,
                    "frais_notaire": frais_notaire,
                    "frais_agence_immo": frais_agence_immo,
                    "frais_courtage": frais_courtage,
                    "frais_syndic": frais_syndic,
                    "frais_divers": frais_divers,
                    "provision_charges": provision_charges,
                })