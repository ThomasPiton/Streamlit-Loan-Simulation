import streamlit as st
import pandas as pd 


st.title("Basic Loan Simulation")

st.markdown("""
### Description

Cette simulation vous permet de calculer les mensualités et le coût total d'un prêt simple. 
Il vous suffit d'entrer le montant du prêt, le taux d'intérêt et la durée du prêt, puis de cliquer sur "Calculer". 
Les résultats afficheront le montant de la mensualité, le coût total du prêt et les intérêts payés.
""")

st.divider()

# revenus = st.number_input("Revenus nets mensuels (€)", min_value=500, max_value=50_000, value=3000, step=100)
# penalites_remb = st.number_input("Pénalités remboursement anticipé (%)", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
# taux_fixe = st.radio("🔄 Type de taux d'intérêt", ["Fixe", "Variable"])
# type_remboursement = st.radio("Type de remboursement", ["Amortissable", "In Fine"])

capital = st.number_input("Montant de l'emprunt (€)", min_value=1000, max_value=10_000_000, value=200_000, step=1)
duree = st.number_input("Durée du prêt (mois)", min_value=1, max_value=400, value=120, step=1)
taux_interet = st.number_input("Taux d’intérêt nominal (%)", min_value=0.1, max_value=20.0, value=3.0, step=0.01)
assurance = st.number_input("Assurance emprunteur (% du capital)", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
frais_dossier = st.number_input("Frais de dossier (€)", min_value=0, max_value=5000, value=1000, step=1)

# Calcul de la mensualité (hors assurance)
taux_mensuel = (taux_interet / 100) / 12
mensualite = capital * (taux_mensuel / (1 - (1 + taux_mensuel) ** -duree))

# Tableau d'amortissement
solde = capital
cumul_interets = 0
cumul_assurance = 0
cumul_total = 0

data = []
for mois in range(1, duree + 1):
    interets = solde * taux_mensuel
    capital_rembourse = mensualite - interets
    assurance_mensuelle = (assurance / 100) * capital / 12
    cout_total = mensualite + assurance_mensuelle
    cumul_interets += interets
    cumul_assurance += assurance_mensuelle
    cumul_total += cout_total
    solde -= capital_rembourse

    data.append([mois, mensualite, assurance_mensuelle, interets, capital_rembourse, cout_total, cumul_interets, cumul_assurance, cumul_total])
    
df = pd.DataFrame(data, columns=["Mois", "Mensualité", "Assurance", "Intérêts", "Capital remboursé", "Coût total", "Cumul Intérêts","Cumul Assurance","Cumul Total"])

# Calcul des coûts totaux
total_interets = df["Intérêts"].sum()
total_assurance = df["Assurance"].sum()
cout_total_pret = total_interets + total_assurance + capital + frais_dossier

# Ratios clés
ratio_frais = (frais_dossier / cout_total_pret) * 100
ratio_interets = (total_interets / cout_total_pret) * 100
ratio_assurance = (total_assurance / cout_total_pret) * 100
ratio_cout_vs_capital = (cout_total_pret / capital) * 100


st.title("Analyse du Prêt")
st.subheader("Paramètres")
st.write("")

col1, col2, col3, col4, col5 = st.columns(5)

def small_metric(label, value):
    st.markdown(f"""
        <div style="text-align:center; font-size:12px; padding:4px; border:1px solid #ddd; border-radius:5px">
            <strong>{label}</strong><br>
            <span style="font-size:14px">{value}</span>
        </div>
    """, unsafe_allow_html=True)

with col1: small_metric("Emprunt", f"{capital:,.0f} €")
with col2: small_metric("Durée", f"{duree} mois")
with col3: small_metric("Taux", f"{taux_interet:,.2} %")
with col4: small_metric("Assurance", f"{assurance:,.2} %")
with col5: small_metric("Frais", f"{frais_dossier:,.0f} €")

st.write("")
st.subheader("Indicateurs")
st.write("")

col1, col2, col3 = st.columns(3)
col1.metric("Coût total du prêt", f"{cout_total_pret:,.0f} €")
col2.metric("Total des intérêts", f"{total_interets:,.0f} €")
col3.metric("Total de l'assurance", f"{total_assurance:,.0f} €")

col4, col5, col6 = st.columns(3)
col4.metric("Part des intérêts", f"{ratio_interets:.2f} %")
col5.metric("Part de l'assurance", f"{ratio_assurance:.2f} %")
col6.metric("Coût total vs Capital", f"{ratio_cout_vs_capital:.2f} %")

col7, col8, col9 = st.columns(3)
col7.metric("Part des frais", f"{ratio_frais:.2f} %")

tab1, tab2, tab3 = st.tabs(["Tableau d'Amortissement", "Évolution des Intérêts", "Accumulation des Coûts"])

with tab1:
    st.write("### Tableau d'Amortissement")
    st.dataframe(df.style.format({"Mensualité": "{:,.2f} €", "Assurance": "{:,.2f} €", "Intérêts": "{:,.2f} €", 
        "Capital remboursé": "{:,.2f} €", "Coût total": "{:,.2f} €", "Cumul Intérêts": "{:,.2f} €","Cumul Assurance": "{:,.2f} €","Cumul Total": "{:,.2f} €"}))
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Télécharger le tableau en CSV", csv, "tableau_amortissement.csv", "text/csv")

with tab2:
    st.write("### Évolution du Coût des Intérêts")
    st.bar_chart(df[["Mois", "Intérêts","Capital remboursé"]].set_index("Mois"))
    
with tab3:
    st.write("### Accumulation des Intérêts et du Coût Total")
    st.area_chart(df[["Mois", "Cumul Intérêts", "Cumul Assurance", "Cumul Total"]].set_index("Mois"))