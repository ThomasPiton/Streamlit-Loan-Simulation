import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Simulation de loyer locatif", layout="wide")

st.title("💰 Simulation de Revenus Locatifs")
st.markdown("Analysez vos **revenus mensuels et annuels** selon différentes hypothèses de location.")

st.header("1️⃣ Paramètres du bien")

col1, col2, col3 = st.columns(3)
with col1:
    nb_chambres = st.number_input("Nombre de chambres", min_value=1, max_value=20, value=3)
with col2:
    loyer_par_chambre = st.number_input("Loyer par chambre (€)", min_value=100, max_value=5000, value=500)
with col3:
    mode_occupation = st.radio("Mode d’occupation", ["Global", "Par chambre"])

# Taux d’occupation
occupation = []
if mode_occupation == "Global":
    taux = st.slider("Taux d’occupation global (%)", 0, 100, 90)
    occupation = [taux / 100] * nb_chambres
else:
    st.subheader("Taux d’occupation par chambre")
    for i in range(nb_chambres):
        taux_i = st.slider(f"Chambre {i+1}", 0, 100, 90, key=f"chambre_{i}")
        occupation.append(taux_i / 100)

# Revenus mensuels
revenus_par_chambre = [loyer_par_chambre * taux for taux in occupation]
revenu_total_mensuel = sum(revenus_par_chambre)
revenu_total_annuel = revenu_total_mensuel * 12

st.header("2️⃣ Résultats")

st.metric("💵 Revenu locatif mensuel", f"{revenu_total_mensuel:,.0f} €")
st.metric("📅 Revenu locatif annuel", f"{revenu_total_annuel:,.0f} €")

# Dataframe récapitulatif
df = pd.DataFrame({
    "Chambre": [f"Chambre {i+1}" for i in range(nb_chambres)],
    "Taux d'occupation": [f"{round(occ*100)}%" for occ in occupation],
    "Loyer brut (€)": [loyer_par_chambre] * nb_chambres,
    "Loyer perçu (€)": revenus_par_chambre,
})
st.dataframe(df, use_container_width=True)

# Graphique: Répartition des loyers par chambre
fig = px.bar(
    df,
    x="Chambre",
    y="Loyer perçu (€)",
    color="Chambre",
    text="Loyer perçu (€)",
    title="💸 Revenus mensuels par chambre",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# Graphique: Impact du taux d’occupation
fig_occ = px.pie(
    df,
    names="Chambre",
    values="Loyer perçu (€)",
    title="📊 Répartition des revenus selon l’occupation",
    template="plotly_white"
)
st.plotly_chart(fig_occ, use_container_width=True)
