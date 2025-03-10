import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from computation import Loan
from display import LoanVisualizer

st.set_page_config(page_title="Calculateur de Crédit Avancé", page_icon="📊", layout="wide")

st.title("📊 Calculateur de Crédit Avancé")

# 📌 Fonction pour créer une section avec un fond coloré
def section_with_background(title, content_function, bg_color="#f4f4f4", title_color="#333333"):
    with st.container():
        st.markdown(
            f'<div style="background-color:{bg_color};padding:15px;border-radius:10px;margin-bottom:15px;box-shadow:0 2px 5px rgba(0,0,0,0.1);">'
            f'<h4 style="margin-bottom:10px;color:{title_color};border-bottom:1px solid rgba(0,0,0,0.1);padding-bottom:8px;">{title}</h4>',
            unsafe_allow_html=True
        )
        content_function()
        st.markdown("</div>", unsafe_allow_html=True)

# Variables globales pour stocker les valeurs des inputs
loan_data = {
    "montant": 100000,
    "duree": 20,
    "type_credit": "Immobilier",
    "apport": 10000,
    "differe": 6,
    "taux_interet": 5.0,
    "taux_fixe": "Fixe",
    "evolution_taux": 0.5,
    "frais_dossier": 500,
    "frais_notaire": 3000,
    "frais_garantie": 1500,
    "assurance_incluse": False,
    "taux_assurance": 0.3,
    "mode_assurance": "Sur capital initial",
    "remb_anticipe": False,
    "montant_max_annuel": 5000,
    "penalite": 1.0,
    "modulation_mensualites": False,
    "revenu_net": 3000,
    "autres_revenus": 500,
    "taux_endettement_avant": 25.0,
    "autres_credits": 0,
    "inflation_attendue": 2.0,
    "rendement_locatif": 4.0,
    "evolution_prix_bien": 2.0
}

# 📌 1. Informations générales du prêt
def general_info():
    loan_data["montant"] = st.number_input("💰 Montant du prêt (€)", min_value=1000, value=loan_data["montant"], step=1000)
    loan_data["duree"] = st.number_input("📅 Durée du prêt (années)", min_value=1, value=loan_data["duree"], step=1)
    loan_data["type_credit"] = st.selectbox("📂 Type de crédit", ["Immobilier", "Consommation", "Auto", "Étudiant", "Professionnel"], index=["Immobilier", "Consommation", "Auto", "Étudiant", "Professionnel"].index(loan_data["type_credit"]))
    loan_data["apport"] = st.number_input("💵 Apport personnel (€)", min_value=0, value=loan_data["apport"], step=1000)
    loan_data["differe"] = st.number_input("⏳ Différé de remboursement (mois)", min_value=0, value=loan_data["differe"], step=1)

section_with_background("📌 Informations générales", general_info, bg_color="#e8f4f8", title_color="#1a5276")

# 📌 2. Taux et coûts du crédit
def credit_costs():
    loan_data["taux_interet"] = st.number_input("📈 Taux d'intérêt annuel (%)", min_value=0.1, value=loan_data["taux_interet"], step=0.1)
    loan_data["taux_fixe"] = st.radio("⚖️ Type de taux", ["Fixe", "Variable"], index=["Fixe", "Variable"].index(loan_data["taux_fixe"]))
    if loan_data["taux_fixe"] == "Variable":
        loan_data["evolution_taux"] = st.slider("📊 Évolution du taux (%) (si variable)", min_value=-2.0, max_value=2.0, value=loan_data["evolution_taux"], step=0.1)
    loan_data["frais_dossier"] = st.number_input("📝 Frais de dossier (€)", min_value=0, value=loan_data["frais_dossier"], step=50)
    loan_data["frais_notaire"] = st.number_input("🏛️ Frais de notaire (€)", min_value=0, value=loan_data["frais_notaire"], step=100)
    loan_data["frais_garantie"] = st.number_input("🔒 Frais de garantie (€)", min_value=0, value=loan_data["frais_garantie"], step=100)

section_with_background("📌 Taux et coûts du crédit", credit_costs, bg_color="#f8eee8", title_color="#7d3c0a")

# 📌 3. Assurance emprunteur
def insurance():
    loan_data["assurance_incluse"] = st.checkbox("✅ Inclure une assurance emprunteur", value=loan_data["assurance_incluse"])
    if loan_data["assurance_incluse"]:
        loan_data["taux_assurance"] = st.number_input("🛡️ Taux d'assurance (%)", min_value=0.0, value=loan_data["taux_assurance"], step=0.1)
        options = ["Sur capital initial", "Sur capital restant dû"]
        loan_data["mode_assurance"] = st.radio("📑 Mode de calcul", options, index=options.index(loan_data["mode_assurance"]))

section_with_background("📌 Assurance emprunteur", insurance, bg_color="#e8f8e8", title_color="#1e5631")

# 📌 4. Remboursement et flexibilité
def repayment_options():
    loan_data["remb_anticipe"] = st.checkbox("💨 Autoriser le remboursement anticipé", value=loan_data["remb_anticipe"])
    if loan_data["remb_anticipe"]:
        loan_data["montant_max_annuel"] = st.number_input("🔄 Montant max remboursable par an (€)", min_value=0, value=loan_data["montant_max_annuel"], step=1000)
        loan_data["penalite"] = st.number_input("⚠️ Pénalité de remboursement (%)", min_value=0.0, value=loan_data["penalite"], step=0.1)
    loan_data["modulation_mensualites"] = st.checkbox("📊 Permettre la modulation des mensualités", value=loan_data["modulation_mensualites"])

section_with_background("📌 Remboursement et flexibilité", repayment_options, bg_color="#f0e8f8", title_color="#4a235a")

# 📌 5. Contexte financier de l'emprunteur
def borrower_financials():
    loan_data["revenu_net"] = st.number_input("💼 Revenu net mensuel (€)", min_value=0, value=loan_data["revenu_net"], step=100)
    loan_data["autres_revenus"] = st.number_input("📈 Revenus annexes (€)", min_value=0, value=loan_data["autres_revenus"], step=50)
    loan_data["taux_endettement_avant"] = st.number_input("📊 Taux d'endettement avant crédit (%)", min_value=0.0, value=loan_data["taux_endettement_avant"], step=0.1)
    loan_data["autres_credits"] = st.number_input("🏦 Mensualités des autres crédits (€)", min_value=0, value=loan_data["autres_credits"], step=100)

section_with_background("📌 Contexte financier", borrower_financials, bg_color="#f8f8e8", title_color="#7d6608")

# 📌 6. Hypothèses économiques et marché
def economic_assumptions():
    loan_data["inflation_attendue"] = st.number_input("📈 Inflation moyenne attendue (%)", min_value=0.0, value=loan_data["inflation_attendue"], step=0.1)
    loan_data["rendement_locatif"] = st.number_input("🏠 Rendement locatif attendu (%)", min_value=0.0, value=loan_data["rendement_locatif"], step=0.1)
    loan_data["evolution_prix_bien"] = st.number_input("📊 Évolution estimée du prix du bien (%)", min_value=-10.0, max_value=10.0, value=loan_data["evolution_prix_bien"], step=0.1)

section_with_background("📌 Hypothèses économiques et marché", economic_assumptions, bg_color="#f8e8f2", title_color="#8e44ad")

# 📌 Simulation et Visualisation
def display_results():
    # Création d'un objet Loan avec les paramètres saisis
    assurance_mode = "capital initial" if loan_data["mode_assurance"] == "Sur capital initial" else "capital restant dû"
    
    loan = Loan(
        montant=loan_data["montant"], 
        taux_interet=loan_data["taux_interet"], 
        duree_annees=loan_data["duree"],
        differe_mois=loan_data["differe"],
        assurance_taux=loan_data["taux_assurance"] if loan_data["assurance_incluse"] else None,
        assurance_mode=assurance_mode,
        frais_dossier=loan_data["frais_dossier"],
        frais_notaire=loan_data["frais_notaire"],
        frais_garantie=loan_data["frais_garantie"]
    )
    
    # Obtention du tableau d'amortissement
    schedule = loan.generate_amortization_schedule()
    
    # Calcul des résumés du prêt
    summary = loan.calculate_loan_summary()
    
    # Création de l'objet visualiseur
    visualizer = LoanVisualizer(loan)
    
    # Affichage des résultats principaux
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💡 Résumé du prêt")
        
        # Affichage des métriques clés
        metrics_col1, metrics_col2 = st.columns(2)
        
        with metrics_col1:
            st.metric("Montant emprunté", f"{summary['Montant emprunté']:,.2f} €")
            st.metric("Mensualité", f"{summary['Mensualité']:,.2f} €")
            st.metric("Coût total du crédit", f"{summary['Coût total du crédit']:,.2f} €")
            st.metric("Durée du prêt", f"{int(summary['Durée totale (années)'])} ans et {summary['Durée totale (mois)'] % 12} mois")
        
        with metrics_col2:
            st.metric("Total des intérêts", f"{summary['Total intérêts']:,.2f} €")
            st.metric("Total assurance", f"{summary['Total assurance']:,.2f} €")
            st.metric("Frais initiaux", f"{summary['Frais initiaux']:,.2f} €")
            st.metric("Pourcentage du coût", f"{summary['Coût du crédit (%)']:.2f}%")
    
    with col2:
        # Calcul du taux d'endettement
        revenu_total = loan_data["revenu_net"] + loan_data["autres_revenus"]
        mensualite = summary["Mensualité"]
        autres_credits = loan_data["autres_credits"]
        taux_endettement = ((mensualite + autres_credits) / revenu_total) * 100
        
        st.subheader("📊 Analyse financière")
        
        # Affichage des métriques financières
        st.metric("Taux d'endettement après crédit", f"{taux_endettement:.2f}%", 
                 delta=f"{taux_endettement - loan_data['taux_endettement_avant']:.2f}%")
        
        if taux_endettement > 35:
            st.warning("⚠️ Attention : Votre taux d'endettement dépasse 35%, ce qui pourrait compliquer l'obtention de votre crédit.")
        else:
            st.success("✅ Votre taux d'endettement est inférieur à 35%, ce qui est favorable pour l'obtention de votre crédit.")
        
        # Capacité d'épargne après crédit
        capacite_epargne = revenu_total - mensualite - autres_credits
        st.metric("Capacité d'épargne mensuelle", f"{capacite_epargne:.2f} €")
        
        if loan_data["type_credit"] == "Immobilier":
            st.info(f"💡 Avec un rendement locatif de {loan_data['rendement_locatif']}%, "
                    f"ce bien pourrait générer environ {(loan_data['montant'] * loan_data['rendement_locatif'] / 100 / 12):.2f}€ de revenus mensuels.")
    
    # Affichage des graphiques
    st.subheader("📈 Visualisations")

    # Tab layout for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Évolution du capital", "Répartition des coûts", "Répartition des mensualités", "Graphiques interactifs"])

    with tab1:
        # Original matplotlib visualization with improved styling
        fig = visualizer.plot_amortization_curve()
        fig.set_size_inches(10, 6)
        fig.set_facecolor('#F0F2F6')
        for ax in fig.axes:
            ax.set_facecolor('#F0F2F6')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(color='#E0E0E0', linestyle='-', linewidth=0.5, alpha=0.7)
        st.pyplot(fig)

    with tab2:
        # Enhanced pie chart
        fig = visualizer.plot_capital_vs_interest()
        fig.set_size_inches(10, 6)
        fig.set_facecolor('#F0F2F6')
        for ax in fig.axes:
            ax.set_facecolor('#F0F2F6')
        st.pyplot(fig)

    with tab3:
        # Enhanced payment breakdown
        fig = visualizer.plot_payment_breakdown()
        fig.set_size_inches(10, 6)
        fig.set_facecolor('#F0F2F6')
        plt.tight_layout()
        st.pyplot(fig)

    with tab4:
        # Interactive Streamlit native charts
        st.subheader("Graphiques interactifs")
        
        # Preparation of data for Streamlit's native charts
        interactive_data = schedule[['Mois', 'Capital restant dû', 'Intérêts cumulés', 'Assurance cumulée']].copy()
        
        # Line chart for capital evolution
        st.subheader("Évolution du capital restant dû")
        st.line_chart(interactive_data.set_index('Mois')['Capital restant dû'], use_container_width=True)
        
        # Area chart for cumulative interest and insurance
        st.subheader("Intérêts et assurance cumulés")
        chart_data = interactive_data.set_index('Mois')[['Intérêts cumulés', 'Assurance cumulée']]
        st.area_chart(chart_data, use_container_width=True)
        
        # Create a comparison chart showing monthly breakdown
        st.subheader("Composition des paiements mensuels")
        monthly_composition = pd.DataFrame({
            'Mois': schedule['Mois'],
            'Capital': schedule['Capital'],
            'Intérêts': schedule['Intérêts'],
            'Assurance': schedule['Assurance']
        }).set_index('Mois')
        
        # Only show every 12th month for clarity if the loan is longer than 5 years
        if loan_data["duree"] > 5:
            monthly_composition = monthly_composition.iloc[::12]
        
        st.bar_chart(monthly_composition, use_container_width=True)

        # Additional interactive visualization
        st.subheader("📊 Analyse comparative")

        # Create columns for side-by-side metrics
        col1, col2 = st.columns(2)

        with col1:
            # Create a gauge chart for debt ratio
            revenu_total = loan_data["revenu_net"] + loan_data["autres_revenus"]
            mensualite = summary["Mensualité"]
            autres_credits = loan_data["autres_credits"]
            taux_endettement = ((mensualite + autres_credits) / revenu_total) * 100
            
            # Visualization using Streamlit metrics and progress bar
            st.metric("Taux d'endettement", f"{taux_endettement:.2f}%")
            st.progress(min(taux_endettement/100, 1.0))
            
            # Color-coded indication of debt ratio status
            if taux_endettement <= 25:
                st.success("✅ Excellent: Moins de 25% d'endettement")
            elif taux_endettement <= 35:
                st.info("ℹ️ Bon: Endettement entre 25% et 35%")
            else:
                st.warning("⚠️ Attention: Endettement supérieur à 35%")

        with col2:
            # Time to recover investment (for real estate)
            if loan_data["type_credit"] == "Immobilier":
                cout_total = loan_data["montant"] + summary['Coût total du crédit']
                rendement_mensuel = loan_data["montant"] * loan_data["rendement_locatif"] / 100 / 12
                mois_retour = cout_total / rendement_mensuel if rendement_mensuel > 0 else float('inf')
                annees_retour = mois_retour / 12
                
                st.metric("Retour sur investissement", f"{annees_retour:.1f} années")
                
                # ROI Visualization
                max_years = 50  # Maximum years to display
                roi_percentage = min(annees_retour / max_years, 1.0)
                st.progress(roi_percentage)
                
                if annees_retour <= 15:
                    st.success("✅ Excellent investissement à long terme")
                elif annees_retour <= 25:
                    st.info("ℹ️ Bon investissement immobilier")
                else:
                    st.warning("⚠️ Rentabilité à très long terme")

# Add this at the end of the file to call the display_results function
section_with_background("📌 Résultats de la simulation", display_results, bg_color="#e8f0f8", title_color="#2874a6")