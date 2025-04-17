import streamlit as st
from pages.investment.components.base_section import BaseSection
from pages.investment.components.data_store import DataStore

class Travaux(BaseSection):

    def render(self):
        with st.expander("2️⃣ Rénovation, Réparations et Estimations de Travaux – *Cliquez pour ouvrir*", expanded=False):
            
            st.subheader("Estimations de Rénovation et Travaux")

            active_renovation = st.checkbox("Activer / Désactiver", key="active_renovation")
            if active_renovation:
                st.success("**Activée**")
            else:
                st.warning("**Désactivée**")

            budget_renovation = st.number_input(
                "Budget Global de Rénovation Estimé (€)", 
                min_value=0, 
                value=20000, 
                step=1000, 
                key="budget_renovation"
            )
            duree_renovation = st.number_input(
                "Durée de Rénovation Estimée (Mois)", 
                min_value=1, 
                value=6, 
                step=1, 
                key="duree_renovation"
            )
            type_renovation = st.selectbox(
                "Type de Rénovation", 
                options=["Légère", "Moyenne", "Lourde"], 
                index=0, 
                key="type_renovation"
            )

            ventilation_active = st.checkbox("Activer la Ventilation par Poste", key="ventilation_active")

            ventilation = {}
            if ventilation_active:
                st.markdown("### Répartition du Budget par Poste")
                ventilation["cuisine"] = st.number_input("Travaux Cuisine (€)", min_value=0, value=5000, step=500, key="travaux_cuisine")
                ventilation["salle_de_bain"] = st.number_input("Travaux Salle de Bain (€)", min_value=0, value=4000, step=500, key="travaux_sdb")
                ventilation["salon"] = st.number_input("Travaux Salon / Séjour (€)", min_value=0, value=2000, step=500, key="travaux_salon")
                ventilation["chambres"] = st.number_input("Travaux Chambres (€)", min_value=0, value=3000, step=500, key="travaux_chambres")
                ventilation["menuiserie"] = st.number_input("Fenêtres / Menuiserie (€)", min_value=0, value=2000, step=500, key="travaux_menuiserie")
                ventilation["electricite"] = st.number_input("Électricité / Mise aux normes (€)", min_value=0, value=2500, step=500, key="travaux_electricite")
                ventilation["peinture"] = st.number_input("Peinture / Revêtements Murs et Sols (€)", min_value=0, value=1500, step=500, key="travaux_peinture")

            st.markdown("### Travaux Déductibles et Amortissables")
            travaux_deductibles = st.number_input("Travaux Déductibles des Revenus Fonciers (€)", min_value=0, value=15000, step=500, key="travaux_deductibles")
            amortissables = st.checkbox("Inclure dans l’Amortissement (LMNP, SCI IS, etc.)", key="travaux_amortissables")

            # Stockage
            if active_renovation:
                DataStore.set("travaux", {
                    "active": active_renovation,
                    "budget_total": budget_renovation,
                    "duree_mois": duree_renovation,
                    "type": type_renovation,
                    "ventilation_active": ventilation_active,
                    "ventilation": ventilation if ventilation_active else {},
                    "fiscalite": {
                        "deductibles": travaux_deductibles,
                        "amortissables": amortissables,
                    }
                })