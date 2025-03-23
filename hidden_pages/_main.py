# # import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from dataclasses import dataclass
# from typing import List, Dict, Optional, Union, Tuple
# from enum import Enum
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# import math

# # Configuration de la page Streamlit
# st.set_page_config(
#     page_title="Simulateur de Crédit",
#     page_icon="💰",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Définition des classes pour la simulation de prêt

# class TypeRemboursement(Enum):
#     AMORTISSEMENT_CONSTANT = "Amortissement constant"
#     ANNUITES_CONSTANTES = "Annuités constantes"
#     IN_FINE = "In fine"


# class FrequenceRemboursement(Enum):
#     MENSUEL = "Mensuel"
#     TRIMESTRIEL = "Trimestriel"
#     SEMESTRIEL = "Semestriel"
#     ANNUEL = "Annuel"


# class TypeDiffere(Enum):
#     AUCUN = "Aucun"
#     PARTIEL = "Différé partiel (intérêts seulement)"
#     TOTAL = "Différé total (aucun paiement)"


# @dataclass
# class LoanParams:
#     montant: float
#     duree_mois: int
#     taux_annuel: float
#     type_remboursement: TypeRemboursement
#     frequence_remboursement: FrequenceRemboursement
#     periode_differe_mois: int = 0
#     type_differe: TypeDiffere = TypeDiffere.AUCUN
#     taux_assurance: float = 0.0
#     frais_dossier: float = 0.0
#     frais_garantie: float = 0.0
#     apport_initial: float = 0.0
#     remboursements_anticipes: Dict[int, float] = None
#     taux_variable: bool = False
#     ajustement_taux: List[Tuple[int, float]] = None
    
#     def __post_init__(self):
#         if self.remboursements_anticipes is None:
#             self.remboursements_anticipes = {}
#         if self.ajustement_taux is None:
#             self.ajustement_taux = []
        
#         # Conversion des fréquences en nombre de mois
#         self.periode_paiement_mois = {
#             FrequenceRemboursement.MENSUEL: 1,
#             FrequenceRemboursement.TRIMESTRIEL: 3,
#             FrequenceRemboursement.SEMESTRIEL: 6,
#             FrequenceRemboursement.ANNUEL: 12
#         }[self.frequence_remboursement]


# class Loan:
#     def __init__(self, params: LoanParams):
#         self.params = params
#         self.tableau_amortissement = None
#         self.calculer_tableau_amortissement()
    
#     def taux_periodique(self, taux_annuel: float) -> float:
#         """Calcule le taux périodique en fonction de la fréquence de remboursement"""
#         periode = self.params.periode_paiement_mois
#         return ((1 + taux_annuel / 100) ** (periode / 12)) - 1
    
#     def calculer_mensualite(self, capital_restant: float, periodes_restantes: int, taux_periodique: float) -> float:
#         """Calcule la mensualité en fonction du type de remboursement"""
#         if self.params.type_remboursement == TypeRemboursement.ANNUITES_CONSTANTES:
#             if taux_periodique == 0:
#                 return capital_restant / periodes_restantes
#             return capital_restant * taux_periodique / (1 - (1 + taux_periodique) ** -periodes_restantes)
#         elif self.params.type_remboursement == TypeRemboursement.AMORTISSEMENT_CONSTANT:
#             amortissement = capital_restant / periodes_restantes
#             interets = capital_restant * taux_periodique
#             return amortissement + interets
#         elif self.params.type_remboursement == TypeRemboursement.IN_FINE:
#             return capital_restant * taux_periodique
    
#     def calculer_tableau_amortissement(self) -> pd.DataFrame:
#         """Calcule le tableau d'amortissement complet"""
#         # Initialisation des variables
#         capital_restant = self.params.montant - self.params.apport_initial
#         taux_annuel_courant = self.params.taux_annuel
#         nb_periodes = math.ceil(self.params.duree_mois / self.params.periode_paiement_mois)
        
#         # Création du tableau d'amortissement
#         data = []
#         periode_courante = 0
#         mois_courant = 0
        
#         while periode_courante < nb_periodes and capital_restant > 0.01:
#             # Vérifier s'il y a un ajustement de taux pour cette période
#             for mois, nouveau_taux in self.params.ajustement_taux:
#                 if mois_courant <= mois < mois_courant + self.params.periode_paiement_mois:
#                     taux_annuel_courant = nouveau_taux
            
#             # Calculer le taux périodique
#             taux_periodique = self.taux_periodique(taux_annuel_courant)
            
#             # Gestion du différé
#             en_differe = mois_courant < self.params.periode_differe_mois
            
#             # Calcul des intérêts
#             interets = capital_restant * taux_periodique
            
#             # Calcul de l'assurance
#             assurance = (self.params.montant - self.params.apport_initial) * (self.params.taux_assurance / 100) * (self.params.periode_paiement_mois / 12)
            
#             # Calcul de l'amortissement et de la mensualité
#             if en_differe:
#                 if self.params.type_differe == TypeDiffere.TOTAL:
#                     amortissement = 0
#                     mensualite = 0
#                 else:  # Différé partiel
#                     amortissement = 0
#                     mensualite = interets + assurance
#             else:
#                 if self.params.type_remboursement == TypeRemboursement.IN_FINE and periode_courante < nb_periodes - 1:
#                     amortissement = 0
#                     mensualite = interets + assurance
#                 else:
#                     periodes_restantes = nb_periodes - periode_courante
#                     if self.params.type_remboursement == TypeRemboursement.ANNUITES_CONSTANTES:
#                         mensualite = self.calculer_mensualite(capital_restant, periodes_restantes, taux_periodique)
#                         amortissement = mensualite - interets
#                     elif self.params.type_remboursement == TypeRemboursement.AMORTISSEMENT_CONSTANT:
#                         amortissement = capital_restant / periodes_restantes
#                         mensualite = amortissement + interets + assurance
#                     elif self.params.type_remboursement == TypeRemboursement.IN_FINE:
#                         amortissement = capital_restant
#                         mensualite = amortissement + interets + assurance
            
#             # Appliquer un remboursement anticipé si défini pour cette période
#             remboursement_anticipe = self.params.remboursements_anticipes.get(periode_courante, 0)
#             if remboursement_anticipe > 0:
#                 amortissement += remboursement_anticipe
#                 mensualite += remboursement_anticipe
            
#             # Mise à jour du capital restant
#             nouveau_capital = capital_restant - amortissement
            
#             # Ajouter la ligne au tableau
#             data.append({
#                 'periode': periode_courante + 1,
#                 'mois': mois_courant + self.params.periode_paiement_mois,
#                 'taux_annuel': taux_annuel_courant,
#                 'taux_periodique': taux_periodique * 100,
#                 'capital_debut': capital_restant,
#                 'mensualite': mensualite,
#                 'interets': interets,
#                 'amortissement': amortissement,
#                 'assurance': assurance,
#                 'remboursement_anticipe': remboursement_anticipe,
#                 'capital_fin': nouveau_capital,
#                 'en_differe': en_differe
#             })
            
#             # Mise à jour pour la prochaine période
#             capital_restant = nouveau_capital
#             periode_courante += 1
#             mois_courant += self.params.periode_paiement_mois
        
#         self.tableau_amortissement = pd.DataFrame(data)
#         return self.tableau_amortissement
    
#     def cout_total(self) -> float:
#         """Calcule le coût total du crédit (intérêts + assurance + frais)"""
#         if self.tableau_amortissement is None:
#             self.calculer_tableau_amortissement()
        
#         interets_total = self.tableau_amortissement['interets'].sum()
#         assurance_total = self.tableau_amortissement['assurance'].sum()
#         frais_total = self.params.frais_dossier + self.params.frais_garantie
        
#         return interets_total + assurance_total + frais_total
    
#     def taux_effectif_global(self) -> float:
#         """Calcule le TEG (Taux Effectif Global)"""
#         cout = self.cout_total()
#         montant_effectif = self.params.montant - self.params.apport_initial
#         duree_annees = self.params.duree_mois / 12
        
#         # Formule simplifiée du TEG
#         return (cout / montant_effectif) / duree_annees * 100
    
#     def mensualite_moyenne(self) -> float:
#         """Calcule la mensualité moyenne"""
#         if self.tableau_amortissement is None:
#             self.calculer_tableau_amortissement()
        
#         return self.tableau_amortissement[self.tableau_amortissement['mensualite'] > 0]['mensualite'].mean()
    
#     def duree_effective(self) -> int:
#         """Calcule la durée effective du prêt en mois"""
#         if self.tableau_amortissement is None:
#             self.calculer_tableau_amortissement()
        
#         return self.tableau_amortissement.iloc[-1]['mois']
    
#     def summary(self) -> Dict:
#         """Retourne un résumé du prêt"""
#         return {
#             'Montant emprunté': f"{self.params.montant - self.params.apport_initial:,.2f} €",
#             'Durée initiale': f"{self.params.duree_mois} mois",
#             'Durée effective': f"{self.duree_effective()} mois",
#             'Taux d\'intérêt initial': f"{self.params.taux_annuel:.2f}%",
#             'Type de remboursement': self.params.type_remboursement.value,
#             'Mensualité moyenne': f"{self.mensualite_moyenne():,.2f} €",
#             'Coût total du crédit': f"{self.cout_total():,.2f} €",
#             'Taux effectif global': f"{self.taux_effectif_global():.2f}%"
#         }


# class StructuredLoan:
#     def __init__(self, loans: List[Loan], name: str = "Prêt structuré"):
#         self.loans = loans
#         self.name = name
    
#     def cout_total(self) -> float:
#         """Calcule le coût total du crédit structuré"""
#         return sum(loan.cout_total() for loan in self.loans)
    
#     def montant_total(self) -> float:
#         """Calcule le montant total emprunté"""
#         return sum(loan.params.montant - loan.params.apport_initial for loan in self.loans)
    
#     def duree_effective(self) -> int:
#         """Retourne la durée maximale parmi les prêts"""
#         return max(loan.duree_effective() for loan in self.loans)
    
#     def taux_effectif_global(self) -> float:
#         """Calcule le TEG du prêt structuré"""
#         cout = self.cout_total()
#         montant = self.montant_total()
#         duree_annees = self.duree_effective() / 12
        
#         return (cout / montant) / duree_annees * 100
    
#     def tableau_amortissement_consolide(self) -> pd.DataFrame:
#         """Combine les tableaux d'amortissement de tous les prêts en un seul"""
#         # Obtenir le mois maximal
#         max_mois = self.duree_effective()
        
#         # Créer un DataFrame avec tous les mois possibles
#         mois_range = range(0, max_mois + 1, 1)
#         df_consolide = pd.DataFrame({'mois': mois_range})
        
#         # Initialiser les colonnes pour les montants
#         df_consolide['mensualite'] = 0.0
#         df_consolide['interets'] = 0.0
#         df_consolide['amortissement'] = 0.0
#         df_consolide['assurance'] = 0.0
#         df_consolide['capital_restant'] = 0.0
        
#         # Ajouter les données de chaque prêt
#         for i, loan in enumerate(self.loans):
#             df = loan.tableau_amortissement
            
#             # Regrouper par mois si nécessaire
#             if 'mois' in df.columns:
#                 df_monthly = df.copy()
#             else:
#                 # Si le tableau est par période plutôt que par mois, on doit convertir
#                 df_monthly = df.copy()
#                 df_monthly['mois'] = df_monthly['periode'] * loan.params.periode_paiement_mois
            
#             # Fusionner avec le tableau consolidé
#             df_monthly_grouped = df_monthly.groupby('mois').agg({
#                 'mensualite': 'sum',
#                 'interets': 'sum',
#                 'amortissement': 'sum',
#                 'assurance': 'sum',
#                 'capital_fin': 'last'
#             }).reset_index()
            
#             # Renommer les colonnes pour ce prêt spécifique
#             loan_cols = {
#                 'mensualite': f'mensualite_pret_{i+1}',
#                 'interets': f'interets_pret_{i+1}',
#                 'amortissement': f'amortissement_pret_{i+1}',
#                 'assurance': f'assurance_pret_{i+1}',
#                 'capital_fin': f'capital_restant_pret_{i+1}'
#             }
#             df_monthly_grouped = df_monthly_grouped.rename(columns=loan_cols)
            
#             # Fusionner avec le tableau consolidé
#             df_consolide = pd.merge(df_consolide, df_monthly_grouped, on='mois', how='left')
            
#             # Ajouter les montants à la somme totale
#             df_consolide['mensualite'] += df_consolide[f'mensualite_pret_{i+1}'].fillna(0)
#             df_consolide['interets'] += df_consolide[f'interets_pret_{i+1}'].fillna(0)
#             df_consolide['amortissement'] += df_consolide[f'amortissement_pret_{i+1}'].fillna(0)
#             df_consolide['assurance'] += df_consolide[f'assurance_pret_{i+1}'].fillna(0)
#             df_consolide['capital_restant'] += df_consolide[f'capital_restant_pret_{i+1}'].fillna(0)
        
#         return df_consolide
    
#     def summary(self) -> Dict:
#         """Retourne un résumé du prêt structuré"""
#         return {
#             'Nombre de prêts': len(self.loans),
#             'Montant total emprunté': f"{self.montant_total():,.2f} €",
#             'Durée effective': f"{self.duree_effective()} mois",
#             'Coût total du crédit': f"{self.cout_total():,.2f} €",
#             'Taux effectif global': f"{self.taux_effectif_global():.2f}%"
#         }


# # Fonctions d'interface utilisateur

# def creer_parametre_loan_basique():
#     """Crée un widget pour les paramètres basiques d'un prêt"""
#     with st.expander("Paramètres du prêt", expanded=True):
#         col1, col2 = st.columns(2)
        
#         with col1:
#             montant = st.number_input("Montant emprunté (€)", min_value=1000.0, max_value=10000000.0, value=100000.0, step=1000.0)
#             duree_annees = st.number_input("Durée (années)", min_value=1, max_value=40, value=20, step=1)
#             duree_mois = duree_annees * 12
#             taux = st.number_input("Taux d'intérêt annuel (%)", min_value=0.1, max_value=20.0, value=3.5, step=0.1)
        
#         with col2:
#             type_remb = st.selectbox(
#                 "Type de remboursement",
#                 options=[tr.value for tr in TypeRemboursement],
#                 index=1
#             )
#             type_remboursement = next(tr for tr in TypeRemboursement if tr.value == type_remb)
            
#             freq_remb = st.selectbox(
#                 "Fréquence de remboursement",
#                 options=[fr.value for fr in FrequenceRemboursement],
#                 index=0
#             )
#             frequence_remboursement = next(fr for fr in FrequenceRemboursement if fr.value == freq_remb)
            
#             assurance = st.number_input("Taux d'assurance annuel (%)", min_value=0.0, max_value=5.0, value=0.36, step=0.01)
    
#     return LoanParams(
#         montant=montant,
#         duree_mois=duree_mois,
#         taux_annuel=taux,
#         type_remboursement=type_remboursement,
#         frequence_remboursement=frequence_remboursement,
#         taux_assurance=assurance
#     )

# def creer_parametre_loan_avance():
#     """Crée un widget pour les paramètres avancés d'un prêt"""
#     with st.expander("Paramètres de base", expanded=True):
#         col1, col2 = st.columns(2)
        
#         with col1:
#             montant = st.number_input("Montant emprunté (€)", min_value=1000.0, max_value=10000000.0, value=200000.0, step=1000.0)
#             duree_annees = st.number_input("Durée (années)", min_value=1, max_value=40, value=20, step=1)
#             duree_mois = duree_annees * 12
#             taux = st.number_input("Taux d'intérêt annuel (%)", min_value=0.1, max_value=20.0, value=3.5, step=0.1)
        
#         with col2:
#             type_remb = st.selectbox(
#                 "Type de remboursement",
#                 options=[tr.value for tr in TypeRemboursement],
#                 index=1
#             )
#             type_remboursement = next(tr for tr in TypeRemboursement if tr.value == type_remb)
            
#             freq_remb = st.selectbox(
#                 "Fréquence de remboursement",
#                 options=[fr.value for fr in FrequenceRemboursement],
#                 index=0
#             )
#             frequence_remboursement = next(fr for fr in FrequenceRemboursement if fr.value == freq_remb)
            
#             assurance = st.number_input("Taux d'assurance annuel (%)", min_value=0.0, max_value=5.0, value=0.36, step=0.01)
    
#     with st.expander("Coûts additionnels et apport"):
#         col1, col2 = st.columns(2)
        
#         with col1:
#             frais_dossier = st.number_input("Frais de dossier (€)", min_value=0.0, max_value=10000.0, value=1000.0, step=100.0)
#             frais_garantie = st.number_input("Frais de garantie (€)", min_value=0.0, max_value=10000.0, value=2000.0, step=100.0)
        
#         with col2:
#             apport = st.number_input("Apport initial (€)", min_value=0.0, max_value=montant, value=0.0, step=1000.0)
    
#     with st.expander("Différé de remboursement"):
#         col1, col2 = st.columns(2)
        
#         with col1:
#             type_diff = st.selectbox(
#                 "Type de différé",
#                 options=[td.value for td in TypeDiffere],
#                 index=0
#             )
#             type_differe = next(td for td in TypeDiffere if td.value == type_diff)
        
#         with col2:
#             if type_differe != TypeDiffere.AUCUN:
#                 periode_differe = st.number_input("Période de différé (mois)", min_value=0, max_value=duree_mois//2, value=6, step=1)
#             else:
#                 periode_differe = 0
    
#     with st.expander("Taux variable"):
#         taux_variable = st.checkbox("Activer le taux variable", value=False)
        
#         ajustement_taux = []
#         if taux_variable:
#             st.write("Définir les ajustements de taux au cours du temps")
#             nb_ajustements = st.number_input("Nombre d'ajustements", min_value=0, max_value=10, value=2, step=1)
            
#             for i in range(nb_ajustements):
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     mois = st.number_input(f"Mois de l'ajustement {i+1}", min_value=1, max_value=duree_mois, value=min(12 * (i+1), duree_mois), step=1, key=f"mois_ajust_{i}")
#                 with col2:
#                     nouveau_taux = st.number_input(f"Nouveau taux {i+1} (%)", min_value=0.1, max_value=20.0, value=taux + 0.5 * (i+1), step=0.1, key=f"taux_ajust_{i}")
#                 ajustement_taux.append((mois, nouveau_taux))
    
#     with st.expander("Remboursements anticipés"):
#         nb_remboursements = st.number_input("Nombre de remboursements anticipés", min_value=0, max_value=10, value=0, step=1)
        
#         remboursements_anticipes = {}
#         for i in range(nb_remboursements):
#             col1, col2 = st.columns(2)
#             with col1:
#                 periode = st.number_input(f"Période du remboursement {i+1}", min_value=1, max_value=duree_mois//frequence_remboursement.periode_paiement_mois, value=12, step=1, key=f"periode_remb_{i}")
#             with col2:
#                 montant_remb = st.number_input(f"Montant du remboursement {i+1} (€)", min_value=1000.0, max_value=montant, value=10000.0, step=1000.0, key=f"montant_remb_{i}")
#             remboursements_anticipes[periode] = montant_remb
    
#     return LoanParams(
#         montant=montant,
#         duree_mois=duree_mois,
#         taux_annuel=taux,
#         type_remboursement=type_remboursement,
#         frequence_remboursement=frequence_remboursement,
#         taux_assurance=assurance,
#         frais_dossier=frais_dossier,
#         frais_garantie=frais_garantie,
#         apport_initial=apport,
#         periode_differe_mois=periode_differe,
#         type_differe=type_differe,
#         taux_variable=taux_variable,
#         ajustement_taux=ajustement_taux,
#         remboursements_anticipes=remboursements_anticipes
#     )

# def afficher_resultats_simulation(loan: Loan):
#     """Affiche les résultats de la simulation"""
#     # Récupérer le résumé du prêt
#     summary = loan.summary()
    
#     # Afficher le résumé dans une grille
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.metric("Mensualité moyenne", summary["Mensualité moyenne"])
    
#     with col2:
#         st.metric("Coût total du crédit", summary["Coût total du crédit"])
    
#     with col3:
#         st.metric("Montant emprunté", summary["Montant emprunté"])
    
#     with col4:
#         st.metric("TEG", summary["Taux effectif global"])
    
#     # Afficher les graphiques et le tableau d'amortissement
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Graphique du coût des intérêts
#         tableau = loan.tableau_amortissement
        
#         # Répartition du coût total
#         interets_total = tableau['interets'].sum()
#         assurance_total = tableau['assurance'].sum()
#         frais_total = loan.params.frais_dossier + loan.params.frais_garantie
        
#         fig1 = go.Figure(data=[
#             go.Pie(
#                 labels=['Capital', 'Intérêts', 'Assurance', 'Frais'],
#                 values=[
#                     loan.params.montant - loan.params.apport_initial,
#                     interets_total,
#                     assurance_total,
#                     frais_total
#                 ],
#                 hole=.3
#             )
#         ])
        
#         fig1.update_layout(
#             title="Répartition du coût total",
#             height=400
#         )
        
#         st.plotly_chart(fig1, use_container_width=True)
    
#     with col2:
#         # Graphique de l'évolution du capital restant
#         fig2 = go.Figure()
        
#         fig2.add_trace(go.Scatter(
#             x=tableau['mois'],
#             y=tableau['capital_fin'],
#             mode='lines',
#             name='Capital restant',
#             line=dict(color='blue')
#         ))
        
#         if loan.params.taux_variable and loan.params.ajustement_taux:
#             for mois, taux in loan.params.ajustement_taux:
#                 fig2.add_vline(x=mois, line_dash="dash", line_color="red",
#                                 annotation_text=f"Taux: {taux}%",
#                                 annotation_position="top right")
        
#         fig2.update_layout(
#             title="Évolution du capital restant",
#             xaxis_title="Mois",
#             yaxis_title="Capital (€)",
#             height=400
#         )
        
#         st.plotly_chart(fig2, use_container_width=True)
    
#     # Tableau des annuités
#     with st.expander("Tableau d'amortissement", expanded=False):
#         # Formatter le tableau pour l'affichage
#         df_display = tableau.copy()
#         if loan.params.frequence_remboursement != FrequenceRemboursement.MENSUEL:
#             df_display['periode'] = df_display['periode'].astype(int)
#             df_display['mois'] = df_display['mois'].astype(int)
        
#         # Formatter les valeurs monétaires
#         for col in ['capital_debut', 'mensualite', 'interets', 'amortissement', 'assurance', 'remboursement_anticipe', 'capital_fin']:
#             df_display[col] = df_display[col].map(lambda x: f"{x:,.2f} €")
        
#         # Formatter les taux
#         df_display['taux_annuel'] = df_display['taux_annuel'].map(lambda x: f"{x:.2f}%")
#         df_display['taux_periodique'] = df_display['taux_periodique'].map(lambda x: f"{x:.4f}%")
        
#         st.dataframe(df_display)

# def simulateur_basic():
#     """Interface du simulateur de crédit basique"""
#     st.title("📊 Simulateur de Crédit Basique")
    
#     # Créer les paramètres du prêt
#     params = creer_parametre_loan_basique()
    
#     # Créer l'objet de prêt
#     loan = Loan(params)
    
#     # Afficher les résultats
#     st.header("Résultats de la simulation")
#     afficher_resultats_simulation(loan)

# def simulateur_avance():
#     """Interface du simulateur de crédit avancé"""
#     st.title("🔍 Simulateur de Crédit Avancé")
    
#     # Créer les paramètres du prêt
#     params = creer_parametre_loan_avance()
    
#     # Créer l'objet de prêt
#     loan = Loan(params)
    
#     # Afficher les résultats
#     st.header("Résultats de la simulation")
#     afficher_resultats_simulation(loan)

# def comparateur_simulations():
#     """Interface du comparateur de simulations"""
#     st.title("🔄 Comparateur de Simulations")
    
#     # Configuration des scénarios
#     nb_scenarios = st.number_input("Nombre de scénarios à comparer", min_value=2, max_value=5, value=2, step=1)
    
#     # Créer les scénarios
#     scenarios = []
#     loan_objects = []
    
#     for i in range(nb_scenarios):
#         with st.expander(f"Scénario {i+1}", expanded=(i == 0)):
#             st.sub