
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta  # Correction: relativedelta sans 's'

from pages.investment.components.data_store import DataStore
from pages.investment.computation.base_compute import BaseCompute

class ComputeLoyer(BaseCompute):
    
    def __init__(self):
        pass
    
    def compute_basic_pret_table(self):
        """
        Crée un DataFrame des paiements quotidiens pour chaque pret.
        
        Args:
            self.self.prets (list): Liste de dictionnaires contenant les informations des self.self.prets
            
        Returns:
            pd.DataFrame: DataFrame avec les paiements quotidiens pour chaque pret
        """
        # Déterminer la date de début et de fin
        dates_debut = [datetime.strptime(pret['date_debut'], '%Y-%m-%d') for pret in self.prets]
        date_debut_min = min(dates_debut)
        
        # Calculer les dates de fin pour chaque prêt
        dates_fin = []
        for i, pret in enumerate(self.prets):
            duree_mois = pret['duree_mois']
            date_debut = dates_debut[i]
            date_fin = date_debut + relativedelta(months=duree_mois)
            dates_fin.append(date_fin)
        
        date_fin_max = max(dates_fin)
        
        # Créer une liste de toutes les dates entre la date de début min et la date de fin max
        jours = pd.date_range(start=date_debut_min, end=date_fin_max, freq='D')
        
        # Initialiser le DataFrame avec les dates
        df = pd.DataFrame({'date': jours})
        
        # Pour chaque prêt, calculer les paiements quotidiens
        for i, pret in enumerate(self.prets):
            nom_pret = pret['pret']  # Supprimer la ponctuation
            montant = pret['montant']
            taux_interet = pret['taux_interet'] / 100  # Convertir en décimal
            duree_mois = pret['duree_mois']
            periodicite = pret['periodicite']
            date_debut = datetime.strptime(pret['date_debut'], '%Y-%m-%d')
            differe = pret.get('differe', {'active': False})
            remboursement_option = pret.get('remboursement_option', "À la date de début du prêt")
            
            # Convertir les remboursements anticipés si les dates sont au format datetime.date
            remboursements_anticipes = []
            for remb in pret.get('remboursements_anticipes', []):
                remb_copie = remb.copy()
                if isinstance(remb['date'], datetime.date):
                    remb_copie['date'] = datetime.combine(remb['date'], datetime.min.time())
                remboursements_anticipes.append(remb_copie)
            
            # Déterminer la fréquence des paiements selon la périodicité
            if periodicite == 'Mensuelle':
                freq = 'MS'  # Month Start
                periodes_par_an = 12
                delta_periode = relativedelta(months=1)
            elif periodicite == 'Trimestrielle':
                freq = 'QS'  # Quarter Start
                periodes_par_an = 4
                delta_periode = relativedelta(months=3)
            elif periodicite == 'Semestrielle':
                freq = '6MS'  # 6 Month Start
                periodes_par_an = 2
                delta_periode = relativedelta(months=6)
            elif periodicite == 'Annuelle':
                freq = 'AS'  # Annual Start
                periodes_par_an = 1
                delta_periode = relativedelta(years=1)
            else:
                # Par défaut mensuel
                freq = 'MS'
                periodes_par_an = 12
                delta_periode = relativedelta(months=1)
            
            # Déterminer la date du premier remboursement selon l'option choisie
            if remboursement_option == "À la date de début du prêt":
                date_premier_remboursement = date_debut
                
            elif remboursement_option == "Au début de la période suivante":
                # Trouver le début de la période suivante
                if periodicite == 'Mensuelle':
                    date_premier_remboursement = date_debut + relativedelta(day=1, months=1)
                elif periodicite == 'Trimestrielle':
                    mois_actuel = date_debut.month
                    mois_prochain_trimestre = 3 * ((mois_actuel - 1) // 3 + 1) + 1
                    if mois_prochain_trimestre > 12:
                        date_premier_remboursement = datetime(date_debut.year + 1, mois_prochain_trimestre - 12, 1)
                    else:
                        date_premier_remboursement = datetime(date_debut.year, mois_prochain_trimestre, 1)
                elif periodicite == 'Semestrielle':
                    mois_actuel = date_debut.month
                    mois_prochain_semestre = 6 * ((mois_actuel - 1) // 6 + 1) + 1
                    if mois_prochain_semestre > 12:
                        date_premier_remboursement = datetime(date_debut.year + 1, mois_prochain_semestre - 12, 1)
                    else:
                        date_premier_remboursement = datetime(date_debut.year, mois_prochain_semestre, 1)
                elif periodicite == 'Annuelle':
                    date_premier_remboursement = datetime(date_debut.year + 1, 1, 1)
                else:
                    date_premier_remboursement = date_debut + relativedelta(day=1, months=1)
                    
            elif remboursement_option == "À la fin de la première période":
                # La fin de la première période à partir de la date de début
                if periodicite == 'Mensuelle':
                    date_premier_remboursement = date_debut + relativedelta(day=31, months=0)
                elif periodicite == 'Trimestrielle':
                    mois_fin_trimestre = 3 * ((date_debut.month - 1) // 3 + 1)
                    date_premier_remboursement = datetime(date_debut.year, mois_fin_trimestre, 1) + relativedelta(day=31)
                elif periodicite == 'Semestrielle':
                    mois_fin_semestre = 6 * ((date_debut.month - 1) // 6 + 1)
                    date_premier_remboursement = datetime(date_debut.year, mois_fin_semestre, 1) + relativedelta(day=31)
                elif periodicite == 'Annuelle':
                    date_premier_remboursement = datetime(date_debut.year, 12, 31)
                else:
                    date_premier_remboursement = date_debut + relativedelta(day=31, months=0)
            else:
                date_premier_remboursement = date_debut
            
            # Calculer le paiement périodique
            taux_par_periode = taux_interet / periodes_par_an
            nombre_paiements = duree_mois / (12 / periodes_par_an)
            
            # Gérer le différé
            duree_differe = 0
            taux_differe = taux_interet
            if differe.get('active', False):
                duree_differe = differe.get('duree', 0)
                taux_differe = differe.get('taux', taux_interet) / 100
                
            # Générer les dates de paiement en tenant compte de la date du premier remboursement
            dates_paiement = [date_premier_remboursement]
            for _ in range(1, int(nombre_paiements)):
                dates_paiement.append(dates_paiement[-1] + delta_periode)
            
            # Créer un DataFrame pour simuler l'amortissement
            amortissement = pd.DataFrame({
                'date_paiement': dates_paiement,
                'paiement': 0.0,
                'interets': 0.0,
                'principal': 0.0,
                'capital_restant': montant
            })
            
            # Simuler le tableau d'amortissement
            capital_restant = montant
            periode_differe = int(duree_differe / (12 / periodes_par_an))
            
            for idx in range(len(amortissement)):
                if idx < periode_differe and differe.get('active', False):
                    # Période de différé
                    type_differe = differe.get('type', '')
                    taux_periode_differe = taux_differe / periodes_par_an
                    
                    if 'Partiel' in type_differe or 'Intérêts' in type_differe:
                        # Paiement des intérêts uniquement
                        amortissement.loc[idx, 'interets'] = capital_restant * taux_periode_differe
                        amortissement.loc[idx, 'principal'] = 0
                        amortissement.loc[idx, 'paiement'] = amortissement.loc[idx, 'interets']
                    elif 'Total' in type_differe:
                        # Aucun paiement (capitalisation des intérêts)
                        amortissement.loc[idx, 'interets'] = capital_restant * taux_periode_differe
                        amortissement.loc[idx, 'principal'] = 0
                        amortissement.loc[idx, 'paiement'] = 0
                        capital_restant += amortissement.loc[idx, 'interets']
                    
                    amortissement.loc[idx, 'capital_restant'] = capital_restant
                else:
                    # Après la période de différé, calculer le paiement normal
                    duree_restante = nombre_paiements - idx
                    
                    if taux_par_periode > 0:
                        paiement_periodique = capital_restant * (taux_par_periode * (1 + taux_par_periode) ** duree_restante) / ((1 + taux_par_periode) ** duree_restante - 1)
                    else:
                        paiement_periodique = capital_restant / duree_restante
                    
                    amortissement.loc[idx, 'interets'] = capital_restant * taux_par_periode
                    amortissement.loc[idx, 'paiement'] = paiement_periodique
                    amortissement.loc[idx, 'principal'] = paiement_periodique - amortissement.loc[idx, 'interets']
                    
                    capital_restant -= amortissement.loc[idx, 'principal']
                    amortissement.loc[idx, 'capital_restant'] = capital_restant
            
            # Appliquer les remboursements anticipés s'ils existent
            if remboursements_anticipes:
                for remb in remboursements_anticipes:
                    date_remb = remb['date'] if isinstance(remb['date'], datetime) else datetime.strptime(remb['date'], '%Y-%m-%d')
                    montant_remb = remb['montant']
                    
                    if montant_remb <= 0:
                        continue  # Ignorer les remboursements de montant 0
                        
                    penalite = remb.get('penalite', 0) / 100
                    montant_penalite = montant_remb * penalite
                    montant_effectif = montant_remb - montant_penalite
                    type_remb = remb.get('type', 'Partiel')
                    
                    # Trouver l'index du paiement après le remboursement anticipé
                    idx_remb = amortissement[amortissement['date_paiement'] > date_remb].index
                    
                    if len(idx_remb) > 0:
                        idx_remb = idx_remb[0]
                        
                        # Récupérer le capital restant au moment du remboursement
                        if idx_remb > 0:
                            capital_restant_avant = amortissement.loc[idx_remb - 1, 'capital_restant']
                        else:
                            capital_restant_avant = montant
                        
                        # Appliquer le remboursement anticipé
                        nouveau_capital = max(0, capital_restant_avant - montant_effectif)
                        
                        if type_remb == 'Total' and nouveau_capital == 0:
                            # Remboursement total: supprimer tous les paiements futurs
                            amortissement = amortissement[:idx_remb].copy()
                            # Ajouter le paiement du remboursement total avec la pénalité
                            amortissement.loc[idx_remb - 1, 'paiement'] += montant_remb
                        else:
                            # Remboursement partiel
                            # Ajouter le paiement de la pénalité
                            if idx_remb > 0:
                                amortissement.loc[idx_remb - 1, 'paiement'] += montant_penalite
                            
                            # Type de remboursement
                            if 'reduction_duree' in type_remb.lower() or 'reduction_duree' in type_remb.lower():
                                # Recalculer le nombre de périodes nécessaires avec la même mensualité
                                paiement_periodique = amortissement.loc[idx_remb, 'paiement']
                                duree_restante = self.calculer_duree_restante(nouveau_capital, taux_par_periode, paiement_periodique)
                                
                                # Supprimer les périodes excédentaires
                                if duree_restante < len(amortissement) - idx_remb:
                                    amortissement = amortissement[:idx_remb + int(duree_restante)].copy()
                            else:
                                # Réduction des mensualités (même durée)
                                duree_restante = len(amortissement) - idx_remb
                                
                                if taux_par_periode > 0:
                                    nouvelle_mensualite = nouveau_capital * (taux_par_periode * (1 + taux_par_periode) ** duree_restante) / ((1 + taux_par_periode) ** duree_restante - 1)
                                else:
                                    nouvelle_mensualite = nouveau_capital / duree_restante
                                
                                # Recalculer le tableau d'amortissement pour les périodes restantes
                                capital_temp = nouveau_capital
                                for j in range(idx_remb, len(amortissement)):
                                    amortissement.loc[j, 'interets'] = capital_temp * taux_par_periode
                                    amortissement.loc[j, 'paiement'] = nouvelle_mensualite
                                    amortissement.loc[j, 'principal'] = nouvelle_mensualite - amortissement.loc[j, 'interets']
                                    capital_temp -= amortissement.loc[j, 'principal']
                                    amortissement.loc[j, 'capital_restant'] = capital_temp
            
            # Créer une série pour ce prêt avec des valeurs quotidiennes de 0
            df[f'frais_{nom_pret}'] = 0.0
            df[f'principal_{nom_pret}'] = 0.0
            df[f'interets_{nom_pret}'] = 0.0
            df[f'paiement_{nom_pret}'] = 0.0
            df[f'capital_restant_{nom_pret}'] = 0.0
            
            # Assigner les valeurs aux dates correspondantes
            for _, row in amortissement.iterrows():
                date_paiement = row['date_paiement']
                idx = df[df['date'] == date_paiement].index
                if len(idx) > 0:
                    df.loc[idx, f'paiement_{nom_pret}'] = row['paiement']
                    df.loc[idx, f'principal_{nom_pret}'] = row['principal']
                    df.loc[idx, f'interets_{nom_pret}'] = row['interets']
                    df.loc[idx, f'capital_restant_{nom_pret}'] = row['capital_restant']
            
            # Interpoler les valeurs pour le capital restant (pour avoir une valeur pour chaque jour)
            derniere_valeur = montant
            for date in df['date']:
                idx = df[df['date'] == date].index[0]
                valeur_actuelle = df.loc[idx, f'capital_restant_{nom_pret}']
                
                if valeur_actuelle == 0:
                    df.loc[idx, f'capital_restant_{nom_pret}'] = derniere_valeur
                else:
                    derniere_valeur = valeur_actuelle
            
            # Trier les valeurs pour assurer la continuité
            df = df.sort_values('date')
            df[f'capital_restant_{nom_pret}'] = df[f'capital_restant_{nom_pret}'].replace(0, method='ffill')
            
            # Frais premier jour    
            frais_premier_jour = (
                pret['frais_dossier_individuel'] +
                pret['frais_courtage_individuel'] +
                pret['frais_divers_pret'] +
                pret['montant'] * pret['frais_caution_individuel'] / 100 +
                pret['montant'] * pret['frais_garantie_hypothecaire'] / 100
            )

            # Étape 2 : Frais à payer chaque année (assurance)
            montant_assurance_annuelle = pret['frais_assurance_individuel']
            
            # Ajout des frais uniques le jour de début du prêt
            idx_debut = df[df['date'] == date_debut].index
            if len(idx_debut) > 0:
                df.loc[idx_debut[0], f'frais_{nom_pret}'] += frais_premier_jour
                
            # Ajout de l'assurance le 31 décembre de chaque année
            dates_31_dec = df[df['date'].dt.month.eq(12) & df['date'].dt.day.eq(31)]

            for idx in dates_31_dec.index:
                df.loc[idx, f'frais_{nom_pret}'] += montant_assurance_annuelle
            
            cols = [f'principal_{nom_pret}', f'interets_{nom_pret}', f'frais_{nom_pret}']
            df[f'paiement_{nom_pret}'] = df[cols].sum(axis=1)
                    
        # Calculer le total des paiements quotidiens pour tous les prêts
        colonnes_paiement = [col for col in df.columns if col.startswith('paiement_')]
        df['paiement_total'] = df[colonnes_paiement].sum(axis=1)
        
        # Calculer les totaux pour principal et intérêts
        colonnes_principal = [col for col in df.columns if col.startswith('principal_')]
        colonnes_interets = [col for col in df.columns if col.startswith('interets_')]
        colonnes_frais = [col for col in df.columns if col.startswith('frais_')]
        colonnes_capital_restant = [col for col in df.columns if col.startswith('capital_restant_')]
        
        if colonnes_principal:
            df['principal_total'] = df[colonnes_principal].sum(axis=1)
        
        if colonnes_interets:
            df['interets_total'] = df[colonnes_interets].sum(axis=1)
            
        if colonnes_frais:
            df['frais_total'] = df[colonnes_frais].sum(axis=1)
            
        if colonnes_capital_restant:
            df['capital_restant_total'] = df[colonnes_capital_restant].sum(axis=1)
        
        return df
    
    def compute_advanced_pret_table(self):
        pass
    
    def _calculer_duree_restante(self, capital, taux, mensualite):
        if taux == 0:
            return capital / mensualite
        
        if mensualite <= capital * taux:
            return float('inf')  # Mensualité insuffisante pour couvrir les intérêts
        
        return np.log(mensualite / (mensualite - capital * taux)) / np.log(1 + taux)
    
        