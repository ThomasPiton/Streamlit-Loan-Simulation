import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Configuration Streamlit
st.set_page_config(page_title="Simulateur Prêt In Fine", page_icon="📊", layout="centered")

st.title("📊 Simulateur de Prêt In Fine")

st.markdown("""
Ce simulateur vous permet de modéliser un **prêt in fine**, où seuls les **intérêts sont payés chaque mois** et le **capital est remboursé en une fois à la fin** du prêt.
""")

# 🧮 Entrée utilisateur
st.sidebar.header("🔧 Paramètres du prêt")
capital = st.sidebar.number_input("💶 Montant du prêt (€)", 1000, 2000000, 100000, step=1000)
taux_annuel = st.sidebar.number_input("📈 Taux d’intérêt annuel (%)", 0.1, 10.0, 2.0, step=0.1)
duree_annees = st.sidebar.slider("📅 Durée du prêt (années)", 1, 30, 10)

# 🔢 Calculs
taux_mensuel = taux_annuel / 100 / 12
nb_mois = duree_annees * 12
interet_mensuel = capital * taux_mensuel
interet_total = interet_mensuel * nb_mois
remboursement_final = capital

# 📋 Résumé
st.subheader("📌 Résumé")
col1, col2 = st.columns(2)
col1.metric("Mensualité (intérêts)", f"{interet_mensuel:,.2f} €")
col1.metric("Durée", f"{duree_annees} ans")
col2.metric("Total intérêts payés", f"{interet_total:,.2f} €")
col2.metric("Remboursement final", f"{remboursement_final:,.2f} €")

# 📅 Échéancier
data = []
cumul_interets = 0
for mois in range(1, nb_mois + 1):
    capital_rembourse = 0
    if mois == nb_mois:
        capital_rembourse = capital
    cumul_interets += interet_mensuel
    data.append({
        "Mois": mois,
        "Année": (mois - 1) // 12 + 1,
        "Mensualité intérêts (€)": interet_mensuel,
        "Capital remboursé (€)": capital_rembourse,
        "Cumul intérêts (€)": cumul_interets
    })

df = pd.DataFrame(data)

# 📈 Graphique interactif Plotly
st.subheader("📈 Visualisation interactive")
df["Cumul intérêts (€)"] = df["Mensualité intérêts (€)"].cumsum()

# 📊 Création des 3 colonnes
col1, col2, col3 = st.columns(3)

# 1️⃣ Intérêts mensuels
with col1:
    fig1 = px.line(
        df,
        x="Mois",
        y="Mensualité intérêts (€)",
        title="Intérêts mensuels constants",
        labels={"Mensualité intérêts (€)": "Intérêts (€)", "Mois": "Mois"},
        color_discrete_sequence=["#1f77b4"]
    )
    fig1.update_layout(
        template="plotly_white",
        xaxis_title="Mois",
        yaxis_title="Intérêts mensuels (€)",
        height=400
    )
    st.plotly_chart(fig1, use_container_width=True)

# 2️⃣ Cumul des intérêts
with col2:
    fig2 = px.line(
        df,
        x="Mois",
        y="Cumul intérêts (€)",
        title="Cumul des intérêts",
        labels={"Cumul intérêts (€)": "Total intérêts cumulés (€)", "Mois": "Mois"},
        markers=False
    )
    # fig2.update_traces(line=dict(color="#ff7f0e", width=3), marker=dict(size=6))
    fig2.update_layout(
        template="plotly_white",
        xaxis_title="Mois",
        yaxis_title="Cumul des intérêts (€)",
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)

# 3️⃣ Remboursement final du capital
with col3:
    df_cap = df[df["Capital remboursé (€)"] > 0]
    fig3 = px.bar(
        df_cap,
        x="Mois",
        y="Capital remboursé (€)",
        title="Remboursement du capital (mois final)",
        labels={"Capital remboursé (€)": "Capital (€)", "Mois": "Mois"},
        # color_discrete_sequence=["#2ca02c"]
    )
    fig3.update_layout(
        template="plotly_white",
        xaxis_title="Mois",
        yaxis_title="Capital remboursé (€)",
        height=400
    )
    st.plotly_chart(fig3, use_container_width=True)

# 📋 Tableau détaillé
with st.expander("📅 Voir l’échéancier complet"):
    st.dataframe(df.style.format({
        "Mensualité intérêts (€)": "{:.2f}",
        "Capital remboursé (€)": "{:.2f}",
        "Cumul intérêts (€)": "{:.2f}"
    }), use_container_width=True)

# 📤 Export Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Echeancier In Fine")
    return output.getvalue()

st.download_button("📥 Télécharger l’échéancier (Excel)", data=to_excel(df),
                   file_name="echeancier_in_fine.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Footer
st.caption("⚠️ Simulation indicative à but pédagogique. Consultez un professionnel pour valider un projet de financement.")
