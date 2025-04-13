import streamlit as st
from pages.investment.display.base_section import BaseSection

class Fisca(BaseSection):
    
    def render(self):
        with st.expander("Fiscalité et Considérations Fiscales", expanded=False):
            st.subheader("Hypothèses Fiscales et de Taxation")
            active_fisca = st.checkbox("Activer / Désactiver", key=f"active_fisca")
            if active_fisca:
                st.success("**Activée**") 
            else: 
                st.warning("**Désactivée**")
            impot_revenu_locatif = st.number_input("Taux d'Imposition sur les Revenus Locatifs (%)", min_value=0.0, max_value=50.0, value=30.0, step=0.1, key=f"impot_revenu_locatif")
            impot_plus_values = st.number_input("Taux d'Imposition sur les Plus-Values (%)", min_value=0.0, max_value=50.0, value=20.0, step=0.1, key=f"impot_plus_values")
            charges_sociales = st.number_input("Charges Sociales sur les Revenus Locatifs (%)", min_value=0.0, max_value=50.0, value=17.5, step=0.1, key=f"charges_sociales")
            deductions_fiscales = st.number_input("Déductions Fiscales sur les Dépenses (€)", min_value=0, value=1000, step=100, key=f"deductions_fiscales")