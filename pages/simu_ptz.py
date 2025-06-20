import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import io
from models.pret_zero.config import *
from models.pret_zero.pret_zero import ComputePretZero
     # Téléchargement Excel
from io import BytesIO
from xlsxwriter import Workbook

# Configuration de la page
st.set_page_config(page_title="Simulateur - Prêt à Taux Zéro", layout="wide")

# Titre principal
st.title("Simulateur de Prêt à Taux Zéro (PTZ)")

st.markdown("#### **Informations sur le logement**")

zone_location = st.selectbox(
    "Zone de localisation du logement",
    options=ZONE,
    help="Zone géographique selon le zonage PTZ"
)

nature_bien = st.selectbox(
    "Nature du bien",
    options=NATURE_BIEN,
    format_func=lambda x: DICT_NATURE_BIEN[x]
)

prix_achat = st.number_input(
    "Prix d'achat du logement (€)",
    min_value=0,
    value=250_000,
    step=1,
    help="Prix total d'acquisition du logement/projet (bien + honoraires)"
)

st.markdown("#### **Situation familiale et financière**")
nb_occupants = st.selectbox(
    "Nombre d'occupants du logement",
    options=list(range(1, 9)) + ["Plus de 8"],
    help="Nombre total de personnes qui occuperont le logement"
)

if nb_occupants == "Plus de 8":
    nb_occupants = st.number_input("Précisez le nombre d'occupants", min_value=9, value=9)

proprietaire_2ans = st.radio(
    "Avez-vous été propriétaire de votre résidence principale au cours des 2 dernières années ?",
    options=[False, True],
    format_func=lambda x: "Non" if not x else "Oui"
)

# Section pour les paramètres de prêt et différé
st.markdown("#### **Paramètres du prêt**")

duree_pret = st.slider(
    "Durée du prêt (années)",
    min_value=10,
    max_value=25,
    value=20,
    help="Durée totale de remboursement du PTZ"
)

differe = st.radio(
    "Souhaitez-vous ajouter un différé à votre PTZ ?",
    options=[False, True],
    format_func=lambda x: "Non" if not x else "Oui"
)

duree_differe = 0
if differe:
    duree_differe = st.slider(
        "Durée du différé (années)",
        min_value=1,
        max_value=10,
        value=1,
        help="Durée totale du différé"
    )
    


# Widget pour la ventilation par occupant
st.subheader("Détail des revenus")
revenus_detail = st.checkbox("Saisir le détail de chaque occupant")

if revenus_detail:
    occupants_data = []
    
    st.markdown("##### **Revenus par occupant**")
    
    # Création d'un tableau plus organisé
    for i in range(int(nb_occupants)):
        with st.expander(f"Occupant {i+1}", expanded=i < 2):  # Les 2 premiers expanded par défaut
            col_nom, col_prenom, col_revenus = st.columns([1, 1, 1])
            
            with col_nom:
                nom = st.text_input(f"Nom", value=f"Occupant{i+1}", key=f"nom_{i}")
            with col_prenom:
                prenom = st.text_input(f"Prénom", value="", key=f"prenom_{i}")
            with col_revenus:
                revenus = st.number_input(
                    f"Revenus fiscaux N-2 (€)",
                    min_value=0,
                    value=0,
                    step=100,
                    key=f"revenus_{i}",
                    help="Revenus fiscaux de référence de l'année N-2"
                )
            
            occupants_data.append({
                "Nom": nom,
                "Prénom": prenom, 
                "Revenus": revenus
            })
    
    rfr = sum([occ["Revenus"] for occ in occupants_data])
    
    # Affichage du récapitulatif des revenus
    if rfr > 0:
        st.success(f"**Total des revenus fiscaux :** {rfr:,.0f} €")
        
        # Tableau récapitulatif
        df_occupants = pd.DataFrame(occupants_data)
        df_occupants['Revenus'] = df_occupants['Revenus'].apply(lambda x: f"{x:,.0f} €")
        st.dataframe(df_occupants, use_container_width=True)
    else:
        st.warning("Veuillez saisir les revenus pour au moins un occupant.")
        
else:
    rfr = st.number_input(
        "Revenus fiscal de référence total de l'année N-2 (€)",
        min_value=0,
        value=45000,
        step=1,
        help="Somme des revenus fiscaux de référence de tous les occupants"
    )

revenu_considere = max(rfr, prix_achat / 9)

# Validation des données avant simulation
st.markdown("---")
st.subheader("Récapitulatif de votre situation")

# Colonnes organisées
recap_col1, recap_col2, recap_col3 = st.columns([1, 1, 1])

with recap_col1:
    st.markdown("### 🏡 Logement")
    st.markdown(f"- **Zone** : `{zone_location}`")
    st.markdown(f"- **Type** : `{DICT_NATURE_BIEN[nature_bien]}`")
    st.markdown(f"- **Prix** : `{prix_achat:,.0f} €`")

with recap_col2:
    st.markdown("### 👨‍👩‍👧‍👦 Foyer")
    st.markdown(f"- **Occupants** : `{nb_occupants}`")
    st.markdown(f"- **Revenus Fiscal de Référence** : `{rfr:,.0f} €`")
    st.markdown(f"- **Revenus Considéré** : `{revenu_considere:,.0f} €`")
    st.markdown(f"- **Propriétaire depuis 2 ans** : `{'Oui' if proprietaire_2ans else 'Non'}`")

with recap_col3:
    st.markdown("### 💶 Prêt")
    st.markdown(f"- **Durée** : `{duree_pret} ans`")
    st.markdown(f"- **Différé** : `{'Oui' if differe else 'Non'}`")
    duree_affichee = f"{duree_differe} ans" if duree_differe > 0 else "N/A"
    st.markdown(f"- **Durée du différé** : `{duree_affichee}`")
    
# Validation des données saisies
erreurs = []
if prix_achat <= 0:
    erreurs.append("Le prix d'achat doit être supérieur à 0 €")
if rfr <= 0:
    erreurs.append("Les revenus totaux doivent être supérieurs à 0 €")
if isinstance(nb_occupants, str):
    erreurs.append("Veuillez préciser le nombre exact d'occupants")

if erreurs:
    for erreur in erreurs:
        st.error(f"❌ {erreur}")

# Bouton de simulation
simulation_possible = len(erreurs) == 0

if simulation_possible:
    if st.button("🚀 Simuler le PTZ", type="primary", use_container_width=True):
        
        # Création de l'instance avec les paramètres saisis
        with st.spinner("Calcul en cours..."):
            try:
                ptz = ComputePretZero(
                    zone_location=zone_location,
                    nb_occupants=int(nb_occupants),
                    nature_bien=nature_bien,
                    proprietaire_2ans=proprietaire_2ans,
                    prix_achat=prix_achat,
                    revenus=revenu_considere,
                    duree_pret=duree_pret,
                    duree_differe=duree_differe
                )
                
                # Exécution de tous les calculs
                resultats = ptz.run()
                
                # Stockage des résultats dans la session pour affichage
                st.session_state['resultats_ptz'] = resultats
                st.session_state['ptz_instance'] = ptz
                st.session_state['simulation_effectuee'] = True
                
                st.success("✅ Simulation effectuée avec succès !")
                st.rerun()  # Rafraîchir la page pour afficher les résultats
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la simulation : {str(e)}")
                st.error("Veuillez vérifier vos paramètres de configuration dans config.py")
else:
    st.button("🚀 Simuler le PTZ", disabled=True, help="Corrigez les erreurs ci-dessus pour effectuer la simulation")

#  Affichage des résultats si la simulation a été effectuée
if 'simulation_effectuee' in st.session_state and st.session_state['simulation_effectuee']:
    st.markdown("---")
    st.header("📊 Résultats de la simulation")
    
    resultats = st.session_state['resultats_ptz']
    ptz_instance = st.session_state['ptz_instance']
    
    # Éligibilité
    if resultats['eligibilite']['eligible']:
        st.success("✅ **Vous êtes éligible au PTZ !**")
        
        # === Résumé du Prêt à Taux Zéro (PTZ) ===
        st.subheader("Résumé du Prêt à Taux Zéro")

        col_ptz1, col_ptz2, col_ptz3, col_ptz4 = st.columns([2, 2, 2, 3])

        with col_ptz1:
            st.metric(
                "Montant PTZ", 
                f"{resultats['ptz']['montant_ptz']:,.0f} €",
                help="Montant maximum du PTZ accordé"
            )

        with col_ptz2:
            st.metric(
                "Quotité", 
                f"{resultats['ptz']['quotite']:.1f} %",
                help="Pourcentage du prix d'achat financé par le PTZ"
            )

        with col_ptz3:
            st.metric(
                "Période de différé", 
                f"{resultats['capital_differe']['periode_differe_annees']} ans",
                help="Durée pendant laquelle vous ne remboursez pas le capital"
            )

        with col_ptz4:
            mensualite_2 = resultats['capital_differe'].get('mensualite_periode2', 0)
            if mensualite_2 > 0:
                st.metric(
                    "Mensualité période 2", 
                    f"{mensualite_2:,.2f} €",
                    help="Mensualité de remboursement après la période de différé"
                )

        # === Situation personnelle ===
        st.markdown("---")
        st.subheader("Situation personnelle")

        col_rev1, col_rev2, col_rev3, col_rev4, col_rev5 = st.columns(5)

        with col_rev1:
            st.metric("Tranche de revenus", resultats['revenus']['tranche_revenus'])

        with col_rev2:
            st.metric("Vos revenus", f"{resultats['revenus']['revenus_total']:,.0f} €")

        with col_rev3:
            st.metric("Plafond applicable", f"{resultats['revenus']['plafond_revenus']:,.0f} €")

        with col_rev4:
            st.metric("Coefficient familial", f"{resultats['ptz']['coefficient_familial']}")

        with col_rev5:
            st.metric("Zone", zone_location)

        st.markdown("---")

        # === Récapitulatif du crédit ===
        st.subheader("Récapitulatif du crédit")

        df_amort = pd.DataFrame(resultats['tableau_amortissement'])
        total_mensualites = df_amort['Mensualité'].sum() if 'Mensualité' in df_amort.columns else 0
        total_interets = df_amort['Intérêts'].sum() if 'Intérêts' in df_amort.columns else 0
        duree_mois = len(df_amort)

        col_res1, col_res2, col_res3, col_res4, col_res5 = st.columns(5)

        with col_res1:
            st.metric("Durée totale", f"{duree_mois} mois")

        with col_res2:
            st.metric("Mensualité", f"{resultats['capital_differe']['mensualite']:,.2f} €")

        with col_res3:
            st.metric("Total mensualités", f"{total_mensualites:,.2f} €")

        with col_res4:
            st.metric("Coût total du crédit", f"{total_mensualites:,.2f} €")

        with col_res5:
            st.metric("Total intérêts", f"{total_interets:,.2f} €")
        
        st.markdown("---")
        # Graphique des quotités par tranche
        st.subheader("Graphiques")
        
        # Graphiques existants
        col1, col2,col3 = st.columns(3)
        
        with col1:
            quotites_par_tranche = [QUOTITES[x][nature_bien] for x in range(1,5)]

            # Couleurs : rouge pour la tranche actuelle, bleu pour les autres
            couleurs = ['red' if i+1 == resultats['revenus']['tranche_revenus'] else 'lightgray' for i in range(4)]
            
            fig_quotites = go.Figure(data=[
                go.Bar(x=TRANCHES, y=quotites_par_tranche, marker_color=couleurs)
            ])
            fig_quotites.update_layout(
                title=f"Quotités par tranche de revenus - Zone {zone_location} - {nature_bien.replace('_', ' ').title()}",
                xaxis_title="Tranche de revenus",
                yaxis_title="Quotité (%)",
                showlegend=False
            )
            st.plotly_chart(fig_quotites, use_container_width=True)
        
        with col2:
            # Graphique en secteurs - Répartition du financement
            labels = ['PTZ', 'Financement personnel']
            values = [resultats['ptz']['montant_ptz'], prix_achat - resultats['ptz']['montant_ptz']]
            colors = ['red', 'lightgray']
            
            fig_pie = go.Figure(
                data=[go.Pie(labels=labels, values=values, hole=0.3,marker=dict(colors=colors))])
            
            fig_pie.update_traces(
                hovertemplate='<b>%{label}</b><br>Montant: %{value:,.0f}€<br>Pourcentage: %{percent}<extra></extra>',
                textinfo='percent',
                textfont_size=12
            )
            fig_pie.update_layout(
                title="Répartition du financement",
                title_font_size=16,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col3:
            # Graphique barres - Coefficients familiaux par nombre d'occupants
            nb_occ_range = list(range(1, 9))
            coefficients = [COEFFICIENT_FAMILIAL[n] for n in nb_occ_range]
            
            # Couleur spéciale pour le coefficient actuel
            couleurs = ['red' if n == int(nb_occupants) else 'lightgray' for n in nb_occ_range]
            
            fig_coeff = go.Figure(data=[
                go.Bar(
                    x=nb_occ_range, 
                    y=coefficients,
                    marker_color=couleurs,
                    text=[f'{coef}' for coef in coefficients],
                    textposition='auto',
                    hovertemplate='<b>%{x} occupant(s)</b><br>Coefficient: %{y}<extra></extra>'
                )
            ])
            fig_coeff.update_layout(
                title="Coefficient familial par nombre d'occupants",
                title_font_size=16,
                xaxis_title="Nombre d'occupants",
                yaxis_title="Coefficient familial",
                xaxis=dict(tickmode='linear', tick0=1, dtick=1),
                yaxis=dict(range=[0, max(coefficients) * 1.1])
            )
            
            st.plotly_chart(fig_coeff, use_container_width=True)
        
        
        col4,col5,col6 = st.columns(3)
        
        with col4:
            # Graphique barres - Coefficients familiaux par nombre d'occupants
            nb_occ_range = list(range(1, 9))
            plafonds = [PLAFONDS_REVENUS[n][zone_location] for n in nb_occ_range]
            
            couleurs = ['red' if n == int(nb_occupants) else 'lightgray' for n in nb_occ_range]
            
            fig_plafond = go.Figure(data=[
                go.Bar(
                    x=nb_occ_range, 
                    y=plafonds,
                    marker_color=couleurs,
                    text=[f"{p:,.0f} €"  for p in plafonds],
                    textposition='outside',  # ✅ Changement ici
                    hovertemplate='<b>%{x} occupant(s)</b><br>Plafond: %{y}<extra></extra>'
                )
            ])
            
            fig_plafond.update_layout(
                title="Plafond de revenus par nombre d'occupants",
                title_font_size=16,
                xaxis_title="Nombre d'occupants",
                yaxis_title="Plafond Revenus (€)",
                xaxis=dict(tickmode='linear', tick0=1, dtick=1),
                yaxis=dict(range=[0, max(plafonds) * 1.1])
            )
            
            st.plotly_chart(fig_plafond, use_container_width=True)

        with col5:
            # Graphique barres - Montants maximum PTZ par zone
            nb_occupants = min(nb_occupants, 5)  # 5 = "plus de 4 occupants"
            montants_zones = [PLAFOND_OPERATION[nb_occupants][z] for z in ZONE]
            
            couleurs_zones = ['red' if z == zone_location else 'lightgray' for z in ZONE]
            
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=ZONE,
                    y=montants_zones,
                    marker_color=couleurs_zones,
                    text=[f"{m:,.0f} €" for m in montants_zones],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Montant: %{y:,.0f} €<extra></extra>'
                )
            ])
            
            fig_bar.update_layout(
                title=f"Montant maximum PTZ par zone pour {nb_occupants} occupant(s)",
                title_font_size=18,
                xaxis_title='Zone',
                yaxis_title='Montant maximum (€)',
                yaxis_tickformat=',.0f',
                uniformtext_minsize=12,
                uniformtext_mode='hide',
                margin=dict(t=60, b=40),
                height=400
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
    
        with col6:
            
            tranche_actuelle = resultats['revenus']['tranche_revenus']
            quotites = QUOTITES[tranche_actuelle]

            natures = [n.replace('_', ' ').title() for n in NATURE_BIEN]
            valeurs = [quotites[n] for n in NATURE_BIEN]

            couleurs = ['red' if n == nature_bien else 'lightgray' for n in NATURE_BIEN]

            fig_quotites = go.Figure(go.Bar(
                x=natures,
                y=valeurs,
                marker_color=couleurs
            ))

            fig_quotites.update_layout(
                title=f"Quotité - Tranche {tranche_actuelle} | Zone {zone_location}",
                xaxis_title="Nature du bien",
                yaxis_title="Quotité (%)",
                showlegend=False,
                yaxis_range=[0, max(valeurs) + 10],
                title_font_size=16
            )

            st.plotly_chart(fig_quotites, use_container_width=True)

        col1, col2 = st.columns(2)
        
        tableau = resultats["tableau_amortissement"]

        # Conversion en DataFrame pour faciliter la manipulation
        df = pd.DataFrame(tableau)

        with col1:
            # 1. Graphique des mensualités dans le temps
            fig_mensualites = go.Figure()

            fig_mensualites.add_trace(go.Scatter(
                x=df['Année'],
                y=df['Mensualité'],
                mode='lines+markers',
                name='Mensualité',
                line=dict(color='red', width=3),
                marker=dict(size=6),
                hovertemplate='<b>Année %{x}</b><br>' +
                            'Mensualité: %{y:,.2f} €<br>' +
                            '<extra></extra>'
            ))

            fig_mensualites.update_layout(
                title={'text': 'Évolution des Mensualités PTZ','x': 0.5},
                xaxis_title='Année',
                yaxis_title='Mensualité (€)',
                template='plotly_white',
                hovermode='x unified',
                height=500,
                font=dict(size=12)
            )

            fig_mensualites.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
            fig_mensualites.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

            st.plotly_chart(fig_mensualites)

        # 2. Graphique du capital remboursé cumulé
        with col2:
            fig_capital = go.Figure()

            fig_capital.add_trace(go.Scatter(
                x=df['Mois'],
                y=df['Capital rembourse cumulé'],
                mode='lines+markers',
                name='Capital remboursé cumulé',
                line=dict(color='red', width=3),
                marker=dict(size=6),
                fill='tonexty',
                fillcolor='rgba(162, 59, 114, 0.1)',
                hovertemplate='<b>Mois %{x}</b><br>' +
                            'Capital remboursé: %{y:,.2f} €<br>' +
                            '<extra></extra>'
            ))

            fig_capital.update_layout(
                title={'text': 'Capital PTZ Remboursé Cumulé','x': 0.5},
                xaxis_title='Mois',
                yaxis_title='Capital remboursé (€)',
                template='plotly_white',
                hovermode='x unified',
                height=500,
                font=dict(size=12)
            )

            fig_capital.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
            fig_capital.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray ')
            st.plotly_chart(fig_capital)

            # 3. Graphique combiné avec deux axes Y
            fig_combine = make_subplots(specs=[[{"secondary_y": True}]])

        # NOUVEAU : Section Tableau d'Amortissement
        st.markdown("---")
        st.subheader("Tableau d'Amortissement PTZ")
        
        if resultats.get('tableau_amortissement') is not None and len(resultats['tableau_amortissement']) > 0:
            # Conversion du tableau en DataFrame pour un meilleur affichage
            import pandas as pd
            
            df_tableau = pd.DataFrame(resultats['tableau_amortissement'])
            
            # Formatage des colonnes numériques
            if 'Mensualité' in df_tableau.columns:
                df_tableau['Mensualité'] = df_tableau['Mensualité'].apply(lambda x: f"{x:,.2f} €" if pd.notnull(x) else "0,00 €")
            if 'Capital remboursé' in df_tableau.columns:
                df_tableau['Capital remboursé'] = df_tableau['Capital remboursé'].apply(lambda x: f"{x:,.2f} €" if pd.notnull(x) else "0,00 €")
            if 'Capital restant' in df_tableau.columns:
                df_tableau['Capital restant'] = df_tableau['Capital restant'].apply(lambda x: f"{x:,.2f} €" if pd.notnull(x) else "0,00 €")
            if 'Intérêts' in df_tableau.columns:
                df_tableau['Intérêts'] = df_tableau['Intérêts'].apply(lambda x: f"{x:,.2f} €" if pd.notnull(x) else "0,00 €")
            
            # Affichage du tableau
            st.dataframe(df_tableau, use_container_width=True, hide_index=True)
            
            
            # Boutons de téléchargement
            col_download1, col_download2, col_download3 = st.columns(3)
            
            with col_download1:
                # Téléchargement CSV
                csv = df_tableau.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 Télécharger en CSV",
                    data=csv,
                    file_name=f"tableau_amortissement_ptz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col_download2:
           
                buffer = BytesIO()
                
                # Reconvertir les valeurs formatées en numériques pour Excel
                df_excel = pd.DataFrame(resultats['tableau_amortissement'])
                
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df_excel.to_excel(writer, sheet_name='Tableau_Amortissement', index=False)
                    
                    # Formatage du fichier Excel
                    workbook = writer.book
                    worksheet = writer.sheets['Tableau_Amortissement']
                    
                    # Format pour les montants
                    money_format = workbook.add_format({'num_format': '#,##0.00 €'})
                    
                    # Application du format aux colonnes monétaires
                    for col_num, col_name in enumerate(df_excel.columns):
                        if col_name in ['Mensualité', 'Capital remboursé', 'Capital restant', 'Intérêts']:
                            worksheet.set_column(col_num, col_num, 15, money_format)
                        else:
                            worksheet.set_column(col_num, col_num, 12)
                
                st.download_button(
                    label="📥 Télécharger en Excel",
                    data=buffer.getvalue(),
                    file_name=f"tableau_amortissement_ptz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col_download3:
                # Téléchargement PDF (optionnel, nécessite reportlab)
                try:
                    from reportlab.lib.pagesizes import A4, landscape
                    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                    from reportlab.lib.styles import getSampleStyleSheet
                    from reportlab.lib import colors
                    
                    buffer_pdf = BytesIO()
                    doc = SimpleDocTemplate(buffer_pdf, pagesize=landscape(A4))
                    
                    # Style du document
                    styles = getSampleStyleSheet()
                    
                    # Titre
                    title = Paragraph("Tableau d'Amortissement PTZ", styles['Title'])
                    
                    # Préparation des données pour le tableau PDF
                    data_pdf = [list(df_excel.columns)]  # En-têtes
                    for _, row in df_excel.iterrows():
                        data_pdf.append([
                            str(row[col]) if col not in ['Mensualité', 'Capital remboursé', 'Capital restant', 'Intérêts'] 
                            else f"{row[col]:,.2f} €" if pd.notnull(row[col]) else "0,00 €"
                            for col in df_excel.columns
                        ])
                    
                    # Création du tableau
                    table = Table(data_pdf)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('FONTSIZE', (0, 1), (-1, -1), 8),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    
                    # Construction du document
                    elements = [title, Spacer(1, 20), table]
                    doc.build(elements)
                    
                    st.download_button(
                        label="📥 Télécharger en PDF",
                        data=buffer_pdf.getvalue(),
                        file_name=f"tableau_amortissement_ptz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                    
                except ImportError:
                    st.info("📄 Téléchargement PDF non disponible (bibliothèque reportlab non installée)")
            
            # Résumé du tableau
            st.markdown("---")
            
                
        else:
            st.warning("⚠️ Aucun tableau d'amortissement disponible")
            st.info("Le tableau d'amortissement sera généré automatiquement lors du calcul du PTZ.")

    else:
        st.error("❌ **Vous n'êtes pas éligible au PTZ**")
        if resultats['eligibilite']['raisons_ineligibilite']:
            st.write("**Raisons de l'inéligibilité :**")
            for raison in resultats['eligibilite']['raisons_ineligibilite']:
                st.write(f"• {raison}")


# Bouton pour réinitialiser la simulation
if 'simulation_effectuee' in st.session_state and st.session_state.simulation_effectuee:
    if st.button("🔄 Nouvelle simulation", type="secondary"):
        # Nettoyer la session
        for key in ['resultats_ptz', 'ptz_instance', 'simulation_effectuee']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()