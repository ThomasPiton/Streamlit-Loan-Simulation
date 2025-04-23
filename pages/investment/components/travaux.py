import streamlit as st
from pages.investment.components.base_section import BaseSection
from pages.investment.components.data_store import DataStore

class Travaux(BaseSection):

    def render(self):
        with st.expander("2️⃣ Travaux, Rénovation et Réparations – *Cliquez pour ouvrir*", expanded=False):
            
            st.subheader("Estimations de Rénovation et Travaux")
            st.divider()
            
            budget_renovation = st.number_input(
                "Budget Global de Rénovation Estimé (€)", 
                min_value=0, 
                value=0, 
                step=1, 
                key="budget_renovation"
            )
            duree_renovation = st.number_input(
                "Durée de Rénovation Estimée (Mois)", 
                min_value=0, 
                value=0, 
                step=1,
                key="duree_renovation"
            )
            type_renovation = st.selectbox(
                "Type de Rénovation", 
                options=["Légère", "Moyenne", "Lourde"], 
                index=0, 
                key="type_renovation"
            )
            
            date_travaux = st.date_input("Date prévue des travaux", key="date_travaux")

            ventilation_active = st.checkbox("Activer la Ventilation par Poste", key="ventilation_active")

            ventilation = {}
            if ventilation_active:
                st.markdown("### Répartition du Budget par Poste")
                ventilation["cuisine"] = st.number_input("Travaux Cuisine (€)", min_value=0, value=0, step=500, key="travaux_cuisine")
                ventilation["salle_de_bain"] = st.number_input("Travaux Salle de Bain (€)", min_value=0, value=0, step=500, key="travaux_sdb")
                ventilation["salon"] = st.number_input("Travaux Salon / Séjour (€)", min_value=0, value=0, step=500, key="travaux_salon")
                ventilation["chambres"] = st.number_input("Travaux Chambres (€)", min_value=0, value=0, step=500, key="travaux_chambres")
                ventilation["menuiserie"] = st.number_input("Fenêtres / Menuiserie (€)", min_value=0, value=0, step=500, key="travaux_menuiserie")
                ventilation["electricite"] = st.number_input("Électricité / Mise aux normes (€)", min_value=0, value=0, step=500, key="travaux_electricite")
                ventilation["peinture"] = st.number_input("Peinture / Revêtements Murs et Sols (€)", min_value=0, value=0, step=500, key="travaux_peinture")

            st.markdown("### Travaux Déductibles et Amortissables")
            travaux_deductibles = st.number_input("Travaux Déductibles des Revenus Fonciers (€)", min_value=0, value=0, step=500, key="travaux_deductibles")
            amortissables = st.checkbox("Inclure dans l’Amortissement (LMNP, SCI IS, etc.)", key="travaux_amortissables")

            # Stockage
            DataStore.set("travaux", {
                "budget_total": budget_renovation,
                "duree_mois": duree_renovation,
                "type": type_renovation,
                "date_travaux":date_travaux,
                "ventilation_active": ventilation_active,
                "ventilation": ventilation if ventilation_active else {},
                "fiscalite": {
                    "deductibles": travaux_deductibles,
                    "amortissables": amortissables,
                }
            })