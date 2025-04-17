import streamlit as st
from datetime import timedelta
from pages.investment.components.data_store import DataStore
from pages.investment.components.base_section import BaseSection

class Loyer(BaseSection):
    
    def render(self):
        with st.expander("4️⃣ Paramètres de Loyer – *Cliquez pour ouvrir*", expanded=False):
    
            label_loyer = [f"Loyer {i+1}" for i in range(5)]
            onglets = st.tabs(label_loyer)
            loyers = []

            # Chaque onglet de loyer
            for i, onglet in enumerate(onglets):
                with onglet:
                    st.subheader(f"Paramètres pour {label_loyer[i]}")

                    active = st.checkbox("Activer / Désactiver", key=f"loyer_activer_{i}")

                    if active:
                        st.success(f"{label_loyer[i]} est **activé**.")
                    else:
                        st.warning(f"{label_loyer[i]} est **désactivé**.")

                    # Entrées de loyer mensuel
                    loyer_mensuel = st.number_input("Montant du Loyer Mensuel (€)", min_value=0, value=1000, step=10, key=f"loyer_mensuel_{i}")
                    charges_mensuelles = st.number_input("Charges Mensuelles (optionnel) (€)", min_value=0, value=0, step=5, key=f"charges_mensuelles_{i}")
                    
                    # Basculement d'entrée de durée
                    utiliser_mois = st.checkbox("Exprimer la Durée en Mois", key=f"utiliser_mois_loyer_{i}")

                    if utiliser_mois:
                        duree_contrat_mois = st.number_input("Durée du Contrat (Mois)", min_value=1, max_value=600, step=1, value=36, key=f"contrat_mois_{i}")
                        duree_contrat_annees = duree_contrat_mois / 12
                    else:
                        duree_contrat_annees = st.number_input("Durée du Contrat (Années)", min_value=1, max_value=50, step=1, value=3, key=f"contrat_annees_{i}")
                        duree_contrat_mois = duree_contrat_annees * 12

                    # Date de début
                    start_date = st.date_input("Date de Début", key=f"start_date_loyer_{i}")
                    end_date = start_date + timedelta(days=int(duree_contrat_mois * 30.4))

                    # Indexation
                    indexation = st.checkbox("Indexation Annuelle?", key=f"indexation_loyer_{i}")

                    # Taux d'occupation
                    st.markdown("#### Taux d'Occupation")
                    mode_occupation = st.radio(
                        "Choisissez comment exprimer l'occupation:",
                        options=["En %", "En mois", "En jours"],
                        horizontal=True,
                        key=f"mode_occupation_{i}"
                    )

                    if mode_occupation == "En %":
                        taux_occupation = st.number_input(
                            "Taux d'Occupation (%)", min_value=0.0, max_value=100.0, value=100.0, step=1.0, key=f"taux_occupation_{i}"
                        )
                        mois_occupes = round(taux_occupation / 100 * 12, 1)
                        jours_occupes = round(taux_occupation / 100 * 365, 1)
                        st.info(f"≈ {mois_occupes} mois ou {jours_occupes} jours occupés par an.")

                    elif mode_occupation == "En mois":
                        mois_occupes = st.number_input(
                            "Nombre de Mois Occupés par An", min_value=0.0, max_value=12.0, value=12.0, step=0.1, key=f"mois_occupes_{i}"
                        )
                        taux_occupation = round(mois_occupes / 12 * 100, 1)
                        jours_occupes = round(mois_occupes * 30.4, 1)
                        st.info(f"≈ {taux_occupation}% ou {jours_occupes} jours occupés par an.")

                    elif mode_occupation == "En jours":
                        jours_occupes = st.number_input(
                            "Nombre de Jours Occupés par An", min_value=0.0, max_value=365.0, value=365.0, step=1.0, key=f"jours_occupes_{i}"
                        )
                        taux_occupation = round(jours_occupes / 365 * 100, 1)
                        mois_occupes = round(jours_occupes / 30.4, 1)
                        st.info(f"≈ {taux_occupation}% ou {mois_occupes} mois occupés par an.")
                        
                    if active:
                        loyers.append(
                            {
                                "label": label_loyer[i],
                                "loyer_mensuel": loyer_mensuel,
                                "charges_mensuelles": charges_mensuelles,
                                "duree_contrat_mois": duree_contrat_mois,
                                "duree_contrat_annees": duree_contrat_annees,
                                "start_date": start_date,
                                "end_date": end_date,
                                "indexation": indexation,
                                "taux_occupation": taux_occupation,
                                "mois_occupes": mois_occupes
                            }
                        )

            # Enregistrement des données dans DataStore
            DataStore.set("loyers", loyers)