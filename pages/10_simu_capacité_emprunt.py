import streamlit as st

# Titre
st.title("Simulation de Capacité d'Emprunt Immobilier")

# Sidebar pour les entrées utilisateur
st.sidebar.header("Paramètres de simulation")

# Entrées utilisateur
revenu_mensuel = st.sidebar.number_input("Revenu mensuel net (€)", min_value=0, step=100, value=3000)
charges_mensuelles = st.sidebar.number_input("Charges mensuelles (€)", min_value=0, step=50, value=500)
taux_endettement_max = st.sidebar.slider("Taux d'endettement maximum (%)", 10, 50, 35)
taux_interet = st.sidebar.slider("Taux d'intérêt annuel (%)", 0.5, 10.0, 2.0, step=0.1)
duree_annees = st.sidebar.slider("Durée du prêt (années)", 5, 30, 20)

# Calcul de la mensualité disponible
mensualite_max = (revenu_mensuel * (taux_endettement_max / 100)) - charges_mensuelles

# Taux mensuel
taux_mensuel = taux_interet / 100 / 12
nb_mois = duree_annees * 12

# Formule de calcul du montant empruntable : mensualité = C * t / (1 - (1 + t)^-n)
if taux_mensuel > 0:
    montant_max = mensualite_max * (1 - (1 + taux_mensuel) ** -nb_mois) / taux_mensuel
else:
    montant_max = mensualite_max * nb_mois  # taux nul

# Affichage des résultats
st.subheader("🧮 Résultat de la simulation")

st.write(f"**Mensualité maximale possible :** {mensualite_max:,.2f} €")
st.write(f"**Montant maximum empruntable :** {montant_max:,.2f} €")
st.write(f"**Durée du prêt :** {duree_annees} ans")
st.write(f"**Taux d’intérêt :** {taux_interet:.2f} %")
st.write(f"**Coût total du crédit estimé :** {mensualite_max * nb_mois - montant_max:,.2f} €")

st.info("⚠️ Simulation indicative. Consultez un conseiller bancaire pour une évaluation précise.")
