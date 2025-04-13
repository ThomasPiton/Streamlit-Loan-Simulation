import streamlit as st
from pages.investment.display.base_section import BaseSection

class Pret(BaseSection):
    
    def render(self):
        with st.expander("Paramètres de Prêt", expanded=False):
    
            label_pret = [f"Prêt {i+1}" for i in range(5)]
            onglets = st.tabs(label_pret)
            prets = []

            # Chaque onglet de prêt
            for i, onglet in enumerate(onglets):
                with onglet:
                    st.subheader(f"Paramètres pour {label_pret[i]}")

                    active = st.checkbox("Activer / Désactiver", key=f"activer_{i}")

                    if active:
                        st.success(f"{label_pret[i]} est **activé**.")
                    else:
                        st.warning(f"{label_pret[i]} est **désactivé**.")

                    montant_pret = st.number_input("Montant du Prêt (€)", min_value=1000, max_value=10_000_000, value=100_000, step=1000, key=f"montant_{i}")
                    taux_interet = st.number_input("Taux d'Intérêt Annuel (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1, key=f"taux_{i}")
                    
                    # Ajouter la sélection du type de remboursement
                    type_remboursement = st.selectbox(
                        "Type de Remboursement", 
                        options=["Amortissable", "Intérêts Seulement", "In Fine"],
                        index=0,
                        key=f"type_remboursement_{i}"
                    )
                    
                    # Basculement d'entrée de durée
                    utiliser_mois = st.checkbox("Exprimer la Durée en Mois", key=f"utiliser_mois_{i}")

                    if utiliser_mois:
                        duree_mois = st.number_input(
                            "Durée du Prêt (Mois)", min_value=1, max_value=600, step=1,
                            value=240, key=f"duree_mois_{i}"
                        )
                        duree_annees = duree_mois / 12
                    else:
                        duree_annees = st.number_input(
                            "Durée du Prêt (Années)", min_value=1, max_value=50, step=1,
                            value=20, key=f"duree_annees_{i}"
                        )
                        duree_mois = duree_annees * 12
                    
                    start_date = st.date_input("Date de Début", key=f"debut_{i}")
                    assurance = st.number_input("Assurance emprunteur (% du capital)", min_value=0.0, max_value=1.0, value=0.1, step=0.01, key=f"assurance_{i}")
                    frais_dossier = st.number_input("Frais de dossier (€)", min_value=0, max_value=5000, value=1000, step=100, key=f"frais_dossier_{i}")