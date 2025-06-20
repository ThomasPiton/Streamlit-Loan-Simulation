import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def calcul_mensualite(montant, taux_annuel, duree_annees):
    taux_mensuel = taux_annuel / 12
    n = duree_annees * 12
    if taux_mensuel == 0:
        mensualite = montant / n
    else:
        mensualite = montant * taux_mensuel / (1 - (1 + taux_mensuel) ** -n)
    cout_total = mensualite * n - montant
    return mensualite, cout_total

st.title("Comparateur de Prêts")

with st.expander("3️⃣ Paramètres de Prêt – *Cliquez pour ouvrir*", expanded=True):
    label_pret = [f"Prêt {i+1}" for i in range(5)]
    onglets = st.tabs(label_pret)
    prets = []

    for i, onglet in enumerate(onglets):
        with onglet:
            st.subheader(f"Paramètres pour {label_pret[i]}")
            st.divider()
            montant = st.number_input("Montant du prêt (€)", min_value=1000, max_value=2_000_000, value=200_000, step=1000, key=f"montant_{i}")
            taux = st.number_input("Taux annuel (%)", min_value=0.0, max_value=10.0, value=1.5, step=0.1, key=f"taux_{i}") / 100
            duree = st.number_input("Durée (années)", min_value=1, max_value=40, value=20, step=1, key=f"duree_{i}")
            active = True if i == 0 else st.checkbox("Activer ce prêt", value=False, key=f"actif_{i}")
            prets.append({"label": label_pret[i], "montant": montant, "taux": taux, "duree": duree, "active": active})

# Filtrage
prets_actifs = [pret for pret in prets if pret["active"]]
if len(prets_actifs) == 0:
    st.warning("Veuillez activer au moins le prêt de référence (Prêt 1).")
    st.stop()

# Calculs
df_resultats = pd.DataFrame([
    {
        "Prêt": pret["label"],
        "Montant (€)": pret["montant"],
        "Taux (%)": pret["taux"] * 100,
        "Durée (années)": pret["duree"],
        "Mensualité (€)": round(calcul_mensualite(pret["montant"], pret["taux"], pret["duree"])[0], 2),
        "Coût total (€)": round(calcul_mensualite(pret["montant"], pret["taux"], pret["duree"])[1], 2),
    }
    for pret in prets_actifs
])

# Calculs complémentaires
df_resultats["Capital remboursé (€)"] = df_resultats["Montant (€)"]
df_resultats["Intérêts (€)"] = df_resultats["Coût total (€)"]
df_resultats["Taux mensuel"] = df_resultats["Taux (%)"] / 100 / 12
df_resultats["Intérêt (€)"] = df_resultats["Montant (€)"] * df_resultats["Taux mensuel"]
df_resultats["Capital (€)"] = df_resultats["Mensualité (€)"] - df_resultats["Intérêt (€)"]

# 📊 Graphiques côte à côte: Répartition Mensualité et Coût Total
st.subheader("📊 Répartition Capital vs Intérêts")

# Mise en page 2 colonnes
col1, col2 = st.columns(2)

# Graphique 1: Répartition de la mensualité (capital vs intérêts)
with col1:
    st.markdown("### Mensualité")
    df_monthly_split = df_resultats[["Prêt", "Capital (€)", "Intérêt (€)"]].melt(
        id_vars="Prêt",
        var_name="Type",
        value_name="Montant"
    )
    fig_monthly = px.bar(
        df_monthly_split, 
        x="Prêt", 
        y="Montant", 
        color="Type",
        title="Composition de la mensualité",
        barmode="stack", 
        template="plotly_white"
    )
    fig_monthly.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        legend_title="",
        height=400,
        xaxis_title="",
        yaxis_title="Montant (€)",
        bargap=0.2
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

# Graphique 2: Répartition du coût total (capital vs intérêts)
with col2:
    st.markdown("### Coût Total")
    df_total_split = df_resultats[["Prêt", "Capital remboursé (€)", "Intérêts (€)"]].melt(
        id_vars="Prêt",
        var_name="Type",
        value_name="Montant"
    )
    fig_total = px.bar(
        df_total_split, 
        x="Prêt", 
        y="Montant", 
        color="Type",
        title="Composition du coût total",
        barmode="stack", 
        template="plotly_white"
    )
    fig_total.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        legend_title="",
        height=400,
        xaxis_title="",
        yaxis_title="Montant (€)",
        bargap=0.2
    )
    st.plotly_chart(fig_total, use_container_width=True)

# 🧾 Résumé des prêts
st.subheader("📊 Résumé des prêts")
st.dataframe(df_resultats, use_container_width=True)

# Comparaison au benchmark
ref = df_resultats.iloc[0]
df_comparaison = df_resultats.copy()
df_comparaison["Diff. Mensualité (€)"] = df_comparaison["Mensualité (€)"] - ref["Mensualité (€)"]
df_comparaison["Diff. Coût total (€)"] = df_comparaison["Coût total (€)"] - ref["Coût total (€)"]

st.subheader("📉 Comparaison par rapport au prêt de référence (Prêt 1)")
st.dataframe(df_comparaison[["Prêt", "Diff. Mensualité (€)", "Diff. Coût total (€)"]], use_container_width=True)

# 📈 Graphiques
st.subheader("📊 Visualisations comparatives des prêts")

# Graphique: Mensualité vs Coût total
fig1 = px.scatter(
    df_resultats,
    x="Mensualité (€)", y="Coût total (€)", color="Prêt", text="Prêt",
    size=6 * np.sqrt(df_resultats["Coût total (€)"]),  # Augmenté ici
    hover_data=["Montant (€)", "Taux (%)", "Durée (années)"],
    title="Mensualité vs Coût total", template="plotly_white"
)
fig1.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
st.plotly_chart(fig1, use_container_width=True)

# Graphique: Mensualité vs Intérêts
fig2 = px.scatter(
    df_resultats,
    x="Mensualité (€)", y="Intérêts (€)", color="Prêt", text="Prêt",
    size=6 * np.sqrt(df_resultats["Intérêts (€)"]),  # Augmenté ici
    hover_data=["Montant (€)", "Taux (%)", "Durée (années)"],
    title="Mensualité vs Intérêts", template="plotly_white"
)
fig2.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
st.plotly_chart(fig2, use_container_width=True)

# Graphique: Durée vs Taux d'intérêt
fig3 = px.scatter(
    df_resultats,
    x="Durée (années)", y="Taux (%)", color="Prêt", text="Prêt",
    size=30 + df_resultats["Mensualité (€)"] / 10,  # Augmenté ici
    hover_data=["Mensualité (€)", "Coût total (€)"],
    title="Durée vs Taux d'intérêt", template="plotly_white"
)
fig3.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
st.plotly_chart(fig3, use_container_width=True) 