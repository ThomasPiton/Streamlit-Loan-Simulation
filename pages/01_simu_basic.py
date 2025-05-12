import streamlit as st
import math

st.title("💰 Simulateur de Prêt Basique")

# --- Champs de saisie ---
st.header("Informations sur le prêt")

montant_loan = st.number_input("Montant du prêt (€)", min_value=1000.0, step=500.0, value=10000.0)
taux_interet = st.number_input("Taux d'intérêt annuel (%)", min_value=0.0, max_value=100.0, value=5.0)
duree_loan_annees = st.number_input("Durée du prêt (années)", min_value=1, max_value=40, value=5)

st.divider()

# --- Calcul ---
if st.button("Simuler le prêt"):
    taux_interet_mensuel = taux_interet / 100 / 12
    nombre_paiements = duree_loan_annees * 12

    # Formule d'amortissement
    if taux_interet_mensuel > 0:
        paiement_mensuel = montant_loan * (taux_interet_mensuel * (1 + taux_interet_mensuel) ** nombre_paiements) / \
                           ((1 + taux_interet_mensuel) ** nombre_paiements - 1)
    else:
        paiement_mensuel = montant_loan / nombre_paiements  # Taux d'intérêt nul

    paiement_total = paiement_mensuel * nombre_paiements
    interets_totaux = paiement_total - montant_loan

    st.success("✅ Résultat de la simulation de prêt")
    st.write(f"**Paiement mensuel :** €{paiement_mensuel:,.2f}")
    st.write(f"**Paiement total :** €{paiement_total:,.2f}")
    st.write(f"**Intérêts totaux payés :** €{interets_totaux:,.2f}")

    # Optionnel : afficher un graphique récapitulatif
    st.subheader("📊 Récapitulatif")
    st.bar_chart({
        "Montant (€)": {
            "Principal": montant_loan,
            "Intérêts": interets_totaux
        }
    })

else:
    st.info("Entrez les informations de votre prêt ci-dessus et cliquez sur **Simuler le prêt**.")
