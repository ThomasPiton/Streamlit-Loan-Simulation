import streamlit as st

# --- Vérification de l'accès ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Vous devez être connecté pour accéder à cette page.")
    st.stop()

st.title("📈 Simulation de Prêt Avancée")

st.markdown("Utilisez cet outil pour affiner votre simulation avec des paramètres détaillés.")

# --- Formulaire d'entrée ---
st.header("Paramètres du prêt")

col1, col2 = st.columns(2)

with col1:
    montant_pret = st.number_input("Montant du prêt (€)", min_value=1000, step=1, value=100000)
    taux_annuel = st.number_input("Taux d'intérêt annuel (%)", min_value=0.0, max_value=100.0,step=0.01, value=1.0)
    duree_annees = st.slider("Durée (années)", 1, 30, 10)

with col2:
    apport = st.number_input("Apport personnel (€)", min_value=0, step=1, value=1000)
    taux_assurance = st.number_input("Taux assurance emprunteur (%)", min_value=0.0, max_value=100.0,step=0.01, value=1.0)
    type_remboursement = st.selectbox("Type de remboursement", ["Mensualités constantes", "Amortissement constant"])

# --- Calcul ---
if st.button("Lancer la simulation"):

    capital_emprunté = montant_pret - apport
    nb_mensualites = duree_annees * 12
    taux_mensuel = taux_annuel / 100 / 12
    taux_assurance_mensuel = taux_assurance / 100 / 12

    if capital_emprunté <= 0:
        st.error("L'apport personnel dépasse ou égale le montant du prêt.")
        st.stop()

    if type_remboursement == "Mensualités constantes":
        if taux_mensuel > 0:
            mensualite = capital_emprunté * (taux_mensuel * (1 + taux_mensuel) ** nb_mensualites) / \
                         ((1 + taux_mensuel) ** nb_mensualites - 1)
        else:
            mensualite = capital_emprunté / nb_mensualites
    else:  # Amortissement constant
        amortissement_constant = capital_emprunté / nb_mensualites
        mensualite = amortissement_constant + (capital_emprunté * taux_mensuel)

    # Assurance mensuelle
    mensualite_assurance = capital_emprunté * taux_assurance_mensuel
    mensualite_totale = mensualite + mensualite_assurance

    total_paye = mensualite_totale * nb_mensualites
    interets_totaux = total_paye - capital_emprunté - (mensualite_assurance * nb_mensualites)

    # --- Résultats ---
    st.success("✅ Résultats de la simulation")

    st.write(f"**Capital emprunté :** €{capital_emprunté:,.2f}")
    st.write(f"**Mensualité (hors assurance) :** €{mensualite:,.2f}")
    st.write(f"**Assurance mensuelle :** €{mensualite_assurance:,.2f}")
    st.write(f"**Mensualité totale :** €{mensualite_totale:,.2f}")
    st.write(f"**Coût total du crédit :** €{total_paye:,.2f}")
    st.write(f"**Intérêts totaux payés :** €{interets_totaux:,.2f}")

    st.subheader("📊 Répartition du coût")
    st.bar_chart({
        "Montant (€)": {
            "Capital": capital_emprunté,
            "Intérêts": interets_totaux,
            "Assurance": mensualite_assurance * nb_mensualites
        }
    })

else:
    st.info("Remplissez les informations ci-dessus puis cliquez sur **Lancer la simulation**.")
