import streamlit as st
from pages.investment.components.base_section import BaseSection
from pages.investment.components.data_store import DataStore

class Charges(BaseSection):
    
    def render(self):
        with st.expander("Dépenses Courantes et Charges Récurrentes", expanded=False):
            st.subheader("Dépenses et Charges Récurrentes")
            active = st.checkbox("Activer / Désactiver", key=f"active")
            if active:
                st.success("**Activée**") 
            else: 
                st.warning("**Désactivée**")

            taxe_fonciere = st.number_input("Taxe Foncière Annuelle (€)", min_value=0, value=1500, step=100, key=f"taxe_fonciere")
            frais_assurance = st.number_input("Frais d'Assurance PNO / Bailleur (€)", min_value=0, value=500, step=50, key=f"frais_assurance")
            frais_gestion = st.number_input("Frais de Gestion Locative (%)", min_value=0.0, max_value=15.0, value=5.0, step=0.1, key=f"frais_gestion")
            frais_entretien = st.number_input("Budget d'Entretien et Réparations (€)", min_value=0, value=1000, step=100, key=f"frais_entretien")
            charges_copro = st.number_input("Charges de Copropriété Annuelles (€)", min_value=0, value=1200, step=100, key=f"charges_copro")
            charges_non_recup = st.number_input("Charges Non Récupérables (€)", min_value=0, value=300, step=50, key=f"charges_non_recup")
            vacance_locative = st.number_input("Taux de Vacance Locative (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.5, key=f"vacance_locative")
            frais_compta = st.number_input("Frais de Comptabilité (LMNP / SCI, €)", min_value=0, value=0, step=100, key=f"frais_compta")
            abonnements = st.number_input("Abonnements / Internet / Alarme (€/an)", min_value=0, value=0, step=100, key=f"abonnements")

            # stocke les paramètres
            if active:
                DataStore.set("charges", {
                    "taxe_fonciere": taxe_fonciere,
                    "frais_assurance": frais_assurance,
                    "frais_gestion": frais_gestion,
                    "frais_entretien": frais_entretien,
                    "charges_copro": charges_copro,
                    "charges_non_recup": charges_non_recup,
                    "vacance_locative": vacance_locative,
                    "frais_compta": frais_compta,
                    "abonnements": abonnements
                })