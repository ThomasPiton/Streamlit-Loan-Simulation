import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Configuration de la page
st.set_page_config(page_title="Simulateur PTZ", page_icon="🏡", layout="centered")

st.title("🏡 Simulateur de Prêt à Taux Zéro (PTZ)")

st.markdown("""
Ce simulateur vous aide à modéliser un **prêt à taux zéro (PTZ)** en tenant compte d'une éventuelle période de **différé total** (aucune mensualité durant une période initiale).
""")

st.sidebar.header("🔧 Paramètres")
montant = st.sidebar.number_input("💶 Montant du prêt (€)", 1000, 200000, 60000, 1000)
duree = st.sidebar.slider("📅 Durée du prêt (ans)", 5, 25, 20)
differe = st.sidebar.slider("⏳ Durée du différé (ans)", 0, duree, 5)

mois_total = duree * 12
mois_differe = differe * 12
mois_remboursement = mois_total - mois_differe

if mois_remboursement > 0:
    mensualite = round(montant / mois_remboursement, 2)
else:
    mensualite = 0

st.subheader("📊 Résumé")
col1, col2 = st.columns(2)
col1.metric("Durée de différé", f"{differe} ans")
col1.metric("Mensualité", f"{mensualite:,.2f} €")
col2.metric("Durée de remboursement", f"{mois_remboursement // 12} ans")
col2.metric("Total remboursé", f"{mensualite * mois_remboursement:,.2f} €")

# Génération échéancier
echeancier = []
cumul = 0
for mois in range(1, mois_total + 1):
    montant_mensuel = 0 if mois <= mois_differe else mensualite
    cumul += montant_mensuel
    echeancier.append({
        "Mois": mois,
        "Année": (mois - 1) // 12 + 1,
        "Mensualité (€)": montant_mensuel,
        "Cumul remboursé (€)": cumul
    })

df = pd.DataFrame(echeancier)

# Graphique interactif avec Plotly
st.subheader("📈 Graphique interactif")
fig = px.line(df, x="Mois", y="Cumul remboursé (€)", title="Cumul du remboursement sur la durée",
              markers=False, labels={"Cumul remboursé (€)": "Cumul (€)"},
              hover_data={"Mensualité (€)": True})

fig.add_bar(x=df["Mois"], y=df["Mensualité (€)"], name="Mensualité", marker_color="lightblue")

fig.update_layout(
    legend=dict(orientation="h", y=-0.2),
    xaxis_title="Mois",
    yaxis_title="Montants (€)",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Échéancier en tableau
with st.expander("📅 Voir l’échéancier détaillé"):
    st.dataframe(df.style.format({"Mensualité (€)": "{:.2f}", "Cumul remboursé (€)": "{:.2f}"}), use_container_width=True)

# Export Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Echéancier')
    return output.getvalue()

excel_bytes = to_excel(df)
st.download_button("📥 Télécharger l’échéancier (Excel)", data=excel_bytes, file_name="echeancier_ptz.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Pied de page
st.caption("⚠️ Simulation indicative. Le PTZ est soumis à des conditions (revenus, zone, type de bien, etc.).")
