import streamlit as st

import streamlit as st

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("You must be logged in to view this page.")
    st.stop()

# Titre de la page
st.title('🏛️ Fiscalité - Immobilier Locatif')

# Introduction
st.markdown("""
Ce guide fournit un aperçu des **charges**, **frais classiques** et **frais exceptionnels** liés à un investissement immobilier locatif. 
Vous y trouverez également des détails sur le traitement fiscal de ces éléments en fonction du régime choisi (IR ou IS).
""")

# Définitions
st.subheader('🔹 Définitions')
st.markdown("""
| **Terme**               | **Définition**                                                       | **Traitement fiscal**                                              |
|-------------------------|-----------------------------------------------------------------------|--------------------------------------------------------------------|
| **Charge**              | Dépense récurrente liée à l'exploitation du bien immobilier.           | Déductible immédiatement (régime réel).                           |
| **Frais classique**     | Dépense ponctuelle liée à l'acquisition ou au financement.            | Non déductible immédiatement, ajouté au prix d'acquisition.        |
| **Frais exceptionnel**  | Dépense rare liée à un événement majeur (travaux lourds, sinistre).   | Immobilisation ou traitement spécifique.                           |
""")

# Charges Déductibles
st.subheader('🔹 Charges - Déductibles immédiatement')
st.markdown("""
Voici des exemples de **charges récurrentes** qui peuvent être déduites immédiatement dans le cadre du régime réel :

- **Assurances** : PNO (propriétaire non occupant), loyers impayés (GLI)
- **Charges de copropriété** : Entretien des parties communes, syndic, nettoyage
- **Entretien courant** : Réparation de plomberie, peinture, électricité
- **Gestion locative** : Frais d'agence, huissier pour relance de loyers impayés
- **Banque** : Frais de gestion de compte, assurance emprunteur
- **Diagnostics** : DPE, électricité, ERP
""")

# Frais Classiques
st.subheader('🔹 Frais classiques - Non déductibles immédiatement')
st.markdown("""
Voici des exemples de **frais ponctuels** liés à l'acquisition du bien :

- **Frais de notaire** : Emoluments, droits d'enregistrement
- **Commission d'agence** : Frais d'achat du bien immobilier
- **Diagnostics pré-achat** : Amiante, plomb, termites
- **Frais bancaires d'acquisition** : Frais de dossier, de garantie
- **Honoraires d'avocat** : Pour la modification de règlement de copropriété
""")

# Frais Exceptionnels
st.subheader('🔹 Frais exceptionnels - Travaux lourds ou événements spéciaux')
st.markdown("""
Voici des exemples de **frais exceptionnels**, liés à des travaux lourds ou à un sinistre :

- **Travaux lourds** : Rénovation de toiture, murs porteurs
- **Création de surface** : Surélévation, extension
- **Sinistres** : Réparations après un incendie ou un dégât des eaux
- **Litiges** : Frais juridiques pour litiges immobiliers
- **Permis** : Frais pour obtenir un permis de construire complexe
""")

# Résumé - Tableau
st.subheader('🎯 Résumé')
st.markdown("""
|  | **Charges**               | **Frais classiques**         | **Frais exceptionnels**     |
|:--|:--|:--|:--|
| **Fréquence**            | Récurrente                   | Ponctuel                    | Rare                        |
| **Nature**               | Fonctionnement courant       | Acquisition                 | Travaux lourds ou litige    |
| **Fiscalité Particulier/SCI IR** | Déductible immédiatement   | Pris en compte à la revente | Pris en compte à la revente |
| **Fiscalité SCI IS**     | Déductible                   | Immobilisation/amortissement| Immobilisation/amortissement|
""")

# À retenir
st.subheader('🔍 À retenir')
st.markdown("""
- **Charges** → Déductibles immédiatement au régime réel.
- **Frais classiques** → Ils augmentent le prix d'acquisition et réduisent la plus-value lors de la revente.
- **Frais exceptionnels** → Immobiliers ou amortis sur plusieurs années, selon leur nature.
""")

