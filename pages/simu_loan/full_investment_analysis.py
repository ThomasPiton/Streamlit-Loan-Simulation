import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Investissement Immobilier", layout="wide")

st.title("Investissement Immobilier")
st.markdown("Description du modèle")
st.divider()

with st.expander("Stratégies d'investissement", expanded=False): 
    st.subheader("Stratégies d'investissement")

    strategies = {
        "Location vide (non meublée)": "Location d’un bien sans mobilier. Bail de 3 ans (renouvelable). Fiscalité en régime foncier réel ou micro-foncier. Moins de rotation mais loyers souvent inférieurs.",
        "Location meublée classique": "Location avec mobilier indispensable. Bail d’un an (ou 9 mois pour étudiants). Fiscalité en LMNP ou LMP, avec amortissements possibles. Rendement souvent plus élevé.",
        "Colocation": "Location à plusieurs locataires. Permet d’optimiser le rendement en louant à la chambre.",
        "Location saisonnière / courte durée": "Location de courte durée (Airbnb). Très rentable mais plus de gestion et réglementation locale possible.",
        "Location étudiante": "Location de septembre à juin. Moins de vacances locatives si proche d'universités.",
        "Location à vocation sociale": "Location à loyers plafonnés (Pinel, Loc’Avantages). Moins rentable mais plus sécurisée fiscalement.",
        "Résidence de services": "Investissement en résidences étudiantes, seniors, affaires, EHPAD. Bail commercial avec exploitant.",
        "Sous-location professionnelle": "Sous-location autorisée via bail commercial. Rentable mais nécessite accord légal.",
        "Immeuble de rapport": "Achat d’un immeuble entier. Mutualise les loyers, maîtrise du bâtiment, plus de gestion.",
        "Achat-revente": "Achat pour revente rapide après travaux. Objectif plus-value immédiate. Très fiscalisé.",
        "Rénovation puis location": "Rachat ancien à rénover pour le louer. Plus-value et déduction fiscale via travaux.",
        "Division immobilière": "Division d’un bien en plusieurs unités. Très rentable mais nécessite mise aux normes.",
        "Nue-propriété / démembrement": "Achat sans usufruit. Pas d’imposition locative pendant plusieurs années. Revalorisation à terme.",
        "Viager": "Achat avec décote contre rente versée au vendeur jusqu'à son décès.",
        "Crowdfunding immobilier": "Placement passif via plateforme. Rendement fixe, sans gestion. Risque de perte en capital.",
        "SCPI": "Placement collectif dans l’immobilier. Revenu régulier, peu de gestion, mais liquidité limitée.",
        "Co-living": "Forme évoluée de la colocation, avec services intégrés. Ciblée jeunes actifs urbains.",
        "Location à des entreprises": "Bail commercial longue durée (3-6-9). Revenus stables mais règles spécifiques.",
        "Location mixte": "Partie habitation + partie pro. Optimisation du rendement.",
        "Immobilier commercial": "Achat de locaux pro (boutiques, bureaux, entrepôts). Stable mais sensible aux cycles."
    }

    selected_strategy = st.selectbox("Choisissez une stratégie d’investissement immobilier :", list(strategies.keys()), key="strategie_invest")

    st.markdown(f"**Description :** {strategies[selected_strategy]}")

# Définir les onglets de loyer
with st.expander("Paramètres de Location", expanded=False):
    
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
                
            # Stocker les informations de loyer si actif
            if active and loyer_mensuel > 0:
                loyers.append({
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
                })
            else:
                loyers.append({
                    "label": label_loyer[i],
                    "active": False
                })

# Définir les onglets de prêt
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
    
# Expander pour les hypothèses de croissance économique et d'inflation
with st.expander("Hypothèses de Croissance Économique et d'Inflation", expanded=False):
    st.subheader("Hypothèses de Croissance et d'Inflation")

    # Activation du contrôle de la croissance et inflation
    active_growth = st.checkbox("Activer / Désactiver la gestion de la Croissance et Inflation", key="active_growth")
    if active_growth:
        st.success("**Activée**") 
    else: 
        st.warning("**Désactivée**")

    # Taux de Croissance Économique Annuel
    st.markdown("### Taux de Croissance Économique Annuel (%)")
    st.markdown("Ce taux représente la croissance attendue de l'économie sur une année. Il est utilisé pour estimer la hausse des revenus, des prix et des autres éléments économiques.")
    taux_croissance_annuel = st.number_input("Taux de Croissance Économique Annuel (%)", 
                                             min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_annuel")

    # Taux d'Inflation Annuel
    st.markdown("### Taux d'Inflation Annuel (%)")
    st.markdown("L'inflation représente l'augmentation générale des prix dans l'économie, ce qui affecte les coûts des biens et services sur une période donnée.")
    taux_inflation = st.number_input("Taux d'Inflation Annuel (%)", 
                                     min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_inflation")

    # Taux d'Augmentation Annuel des Loyers
    st.markdown("### Taux d'Augmentation Annuel des Loyers (%)")
    st.markdown("Ce taux indique la hausse moyenne des loyers sur une année, en fonction de l'inflation et des conditions économiques du marché immobilier.")
    taux_augmentation_loyer = st.number_input("Taux d'Augmentation Annuel des Loyers (%)", 
                                              min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_augmentation_loyer")
    
    # Croissance du Prix au M²
    st.markdown("### Croissance du Prix au M² (%)")
    st.markdown("Indique l'augmentation estimée du prix du mètre carré dans la région concernée. Cela peut refléter l'appréciation du bien immobilier dans un marché en croissance.")
    taux_croissance_prix_m2 = st.number_input("Croissance du Prix au M² (%)", 
                                              min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_prix_m2")

    # Croissance des Charges de Copropriété
    st.markdown("### Croissance des Charges de Copropriété (%)")
    st.markdown("Ce taux représente l'augmentation des charges annuelles de copropriété (syndic, entretien, etc.). Ces charges peuvent être impactées par l'inflation ou les décisions de la copropriété.")
    taux_croissance_charges_copro = st.number_input("Croissance des Charges de Copropriété (%)", 
                                                    min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_charges_copro")

    # Croissance de la Taxe Foncière
    st.markdown("### Croissance de la Taxe Foncière (%)")
    st.markdown("Cette taxe locale peut augmenter au fil du temps, généralement en lien avec les ajustements fiscaux locaux ou l'inflation générale.")
    taux_croissance_taxe_fonciere = st.number_input("Croissance de la Taxe Foncière (%)", 
                                                    min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_taxe_fonciere")

    # Croissance des Frais d'Entretien
    st.markdown("### Croissance des Frais d'Entretien (%)")
    st.markdown("Estime l'augmentation des coûts d'entretien de la propriété (réparations, maintenance, nettoyage, etc.), en fonction des tendances économiques.")
    taux_croissance_entretien = st.number_input("Croissance des Frais d'Entretien (%)", 
                                                min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_entretien")

    # Croissance du Coût de l'Assurance PNO
    st.markdown("### Croissance du Coût de l'Assurance PNO (%)")
    st.markdown("Représente l'augmentation du coût de l'assurance propriétaire non occupant (PNO), souvent en fonction de l'inflation et des risques associés à la propriété.")
    taux_croissance_assurance_pno = st.number_input("Croissance du Coût de l'Assurance PNO (%)", 
                                                     min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_assurance_pno")

    # Croissance du Coût de l'Assurance Emprunteur
    st.markdown("### Croissance du Coût de l'Assurance Emprunteur (%)")
    st.markdown("Si l'assurance emprunteur est révisée périodiquement, ce taux indique l'augmentation attendue de cette assurance, souvent liée à des facteurs comme l'âge ou l'état de santé.")
    taux_croissance_assurance_emprunteur = st.number_input("Croissance du Coût de l'Assurance Emprunteur (%)", 
                                                           min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_assurance_emprunteur")

    # Croissance des Travaux
    st.markdown("### Croissance des Coûts des Travaux (%)")
    st.markdown("L'inflation dans le secteur de la construction peut entraîner une hausse des coûts des travaux futurs (réparations, rénovations, etc.).")
    taux_croissance_cout_travaux = st.number_input("Croissance des Coûts des Travaux (%)", 
                                                   min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_cout_travaux")

    # Taux d'Actualisation
    st.markdown("### Taux d'Actualisation (%)")
    st.markdown("Le taux d'actualisation est utilisé pour déterminer la valeur actuelle des flux futurs. Il est souvent égal à l'inflation plus une prime de rendement.")
    taux_actualisation = st.number_input("Taux d'Actualisation (%)", 
                                         min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_actualisation")

    # Croissance des Revenus Personnels
    st.markdown("### Croissance des Revenus Personnels (%)")
    st.markdown("Estime l'évolution annuelle de tes revenus personnels (salaires, dividendes, etc.), ce qui peut affecter ta capacité d'épargne et ta situation fiscale.")
    taux_croissance_revenus = st.number_input("Croissance des Revenus Personnels (%)", 
                                              min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="taux_croissance_revenus")
    
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