import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

from pages.investment.computation.base_compute import BaseCompute

class ComputePretV2(BaseCompute):
    
    def __init__(self):
        pass # Appel au constructeur parent pour initialiser les données
    
    def compute_basic_pret_table(self):
        """
        Crée un DataFrame des paiements quotidiens pour chaque prêt de manière optimisée.
        
        Returns:
            pd.DataFrame: DataFrame avec les paiements quotidiens pour chaque prêt
        """
        # Déterminer les dates extrêmes pour tous les prêts
        dates_debut = [datetime.strptime(pret['date_debut'], '%Y-%m-%d') for pret in self.prets]
        date_debut_min = min(dates_debut)
        
        # Calculer les dates de fin en une seule passe
        dates_fin = [date_debut + relativedelta(months=pret['duree_mois']) 
                     for date_debut, pret in zip(dates_debut, self.prets)]
        date_fin_max = max(dates_fin)
        
        # Créer la plage de dates une seule fois
        jours = pd.date_range(start=date_debut_min, end=date_fin_max, freq='D')
        df = pd.DataFrame({'date': jours})
        
        # Dictionnaires pour stocker les périodicités et intervalles
        periodicite_map = {
            'Mensuelle': {'freq': 'MS', 'periodes_par_an': 12, 'delta': relativedelta(months=1)},
            'Trimestrielle': {'freq': 'QS', 'periodes_par_an': 4, 'delta': relativedelta(months=3)},
            'Semestrielle': {'freq': '6MS', 'periodes_par_an': 2, 'delta': relativedelta(months=6)},
            'Annuelle': {'freq': 'AS', 'periodes_par_an': 1, 'delta': relativedelta(years=1)}
        }
        
        # Parcourir chaque prêt une seule fois
        for i, pret in enumerate(self.prets):
            # Extraire les informations du prêt
            nom_pret = pret['pret']
            montant = pret['montant']
            taux_interet = pret['taux_interet'] / 100
            duree_mois = pret['duree_mois']
            date_debut = dates_debut[i]
            differe = pret.get('differe', {'active': False})
            remboursement_option = pret.get('remboursement_option', "À la date de début du prêt")
            
            # Obtenir les informations de périodicité
            periodicite = pret['periodicite']
            info_periodicite = periodicite_map.get(periodicite, periodicite_map['Mensuelle'])
            periodes_par_an = info_periodicite['periodes_par_an']
            delta_periode = info_periodicite['delta']
            
            # Déterminer la date du premier remboursement (optimisé)
            date_premier_remboursement = self._calculer_date_premier_remboursement(
                date_debut, periodicite, remboursement_option)
            
            # Générer les dates de paiement de manière plus efficace
            nb_periodes = int(duree_mois / (12 / periodes_par_an))
            dates_paiement = [date_premier_remboursement + (delta_periode * i) for i in range(nb_periodes)]
            
            # Calculer les paramètres du prêt
            taux_par_periode = taux_interet / periodes_par_an
            
            # Simuler l'amortissement en une seule opération vectorisée si possible
            amortissement = self._calculer_tableau_amortissement(
                montant, taux_par_periode, nb_periodes, dates_paiement, differe)
            
            # Appliquer les remboursements anticipés
            amortissement = self._appliquer_remboursements_anticipes(
                amortissement, pret.get('remboursements_anticipes', []), taux_par_periode)
            
            # Créer les colonnes pour ce prêt
            colonnes_pret = [f'frais_{nom_pret}', f'principal_{nom_pret}', 
                             f'interets_{nom_pret}', f'paiement_{nom_pret}', 
                             f'capital_restant_{nom_pret}']
            for col in colonnes_pret:
                df[col] = 0.0
            
            # Remplir les données du tableau d'amortissement dans le DataFrame principal
            self._remplir_dataframe(df, amortissement, nom_pret, montant)
            
            # Calculer et ajouter les frais du prêt
            self._ajouter_frais_pret(df, pret, date_debut, nom_pret)
            
            # Recalculer le paiement total pour ce prêt
            cols = [f'principal_{nom_pret}', f'interets_{nom_pret}', f'frais_{nom_pret}']
            df[f'paiement_{nom_pret}'] = df[cols].sum(axis=1)
        
        # Calculer tous les totaux à la fin
        self._calculer_totaux(df)
        
        return df
    
    def _calculer_date_premier_remboursement(self, date_debut, periodicite, option):
        """Calcule la date du premier remboursement selon l'option choisie"""
        if option == "À la date de début du prêt":
            return date_debut
            
        elif option == "Au début de la période suivante":
            if periodicite == 'Mensuelle':
                return date_debut + relativedelta(day=1, months=1)
            elif periodicite == 'Trimestrielle':
                mois_actuel = date_debut.month
                mois_prochain_trimestre = 3 * ((mois_actuel - 1) // 3 + 1) + 1
                if mois_prochain_trimestre > 12:
                    return datetime(date_debut.year + 1, mois_prochain_trimestre - 12, 1)
                else:
                    return datetime(date_debut.year, mois_prochain_trimestre, 1)
            elif periodicite == 'Semestrielle':
                mois_actuel = date_debut.month
                mois_prochain_semestre = 6 * ((mois_actuel - 1) // 6 + 1) + 1
                if mois_prochain_semestre > 12:
                    return datetime(date_debut.year + 1, mois_prochain_semestre - 12, 1)
                else:
                    return datetime(date_debut.year, mois_prochain_semestre, 1)
            elif periodicite == 'Annuelle':
                return datetime(date_debut.year + 1, 1, 1)
            else:
                return date_debut + relativedelta(day=1, months=1)
                
        elif option == "À la fin de la première période":
            if periodicite == 'Mensuelle':
                return date_debut + relativedelta(day=31, months=0)
            elif periodicite == 'Trimestrielle':
                mois_fin_trimestre = 3 * ((date_debut.month - 1) // 3 + 1)
                return datetime(date_debut.year, mois_fin_trimestre, 1) + relativedelta(day=31)
            elif periodicite == 'Semestrielle':
                mois_fin_semestre = 6 * ((date_debut.month - 1) // 6 + 1)
                return datetime(date_debut.year, mois_fin_semestre, 1) + relativedelta(day=31)
            elif periodicite == 'Annuelle':
                return datetime(date_debut.year, 12, 31)
            else:
                return date_debut + relativedelta(day=31, months=0)
        else:
            return date_debut
    
    def _calculer_tableau_amortissement(self, montant, taux_par_periode, nombre_paiements, 
                                        dates_paiement, differe):
        """Calcule le tableau d'amortissement de manière optimisée"""
        # Initialiser le DataFrame d'amortissement
        amortissement = pd.DataFrame({
            'date_paiement': dates_paiement,
            'paiement': 0.0,
            'interets': 0.0,
            'principal': 0.0,
            'capital_restant': montant  # Valeur initiale
        })
        
        capital_restant = montant
        duree_differe = 0
        taux_differe = taux_par_periode * 100  # Convertir en pourcentage pour le différé
        
        # Gérer le différé
        if differe.get('active', False):
            duree_differe = differe.get('duree', 0)
            taux_differe = differe.get('taux', taux_differe) / 100  # Convertir en décimal
            periode_differe = int(duree_differe / (12 / (100 / taux_par_periode)))
        else:
            periode_differe = 0
            
        # Pré-calculer la mensualité hors période de différé
        if taux_par_periode > 0:
            paiement_periodique = montant * (taux_par_periode * (1 + taux_par_periode) ** 
                                           (nombre_paiements - periode_differe)) / \
                                ((1 + taux_par_periode) ** (nombre_paiements - periode_differe) - 1)
        else:
            paiement_periodique = montant / (nombre_paiements - periode_differe)
        
        # Remplir le tableau d'amortissement
        for idx in range(len(amortissement)):
            if idx < periode_differe and differe.get('active', False):
                # Période de différé
                type_differe = differe.get('type', '')
                taux_periode_differe = taux_differe / (100 / taux_par_periode)
                
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
                # Calcul normal post-différé
                amortissement.loc[idx, 'interets'] = capital_restant * taux_par_periode
                amortissement.loc[idx, 'paiement'] = paiement_periodique
                amortissement.loc[idx, 'principal'] = paiement_periodique - amortissement.loc[idx, 'interets']
                
                capital_restant -= amortissement.loc[idx, 'principal']
                amortissement.loc[idx, 'capital_restant'] = capital_restant
        
        return amortissement
    
    def _appliquer_remboursements_anticipes(self, amortissement, remboursements_anticipes, taux_par_periode):
        """Applique les remboursements anticipés au tableau d'amortissement"""
        if not remboursements_anticipes:
            return amortissement
            
        # Trier les remboursements par date
        remboursements_anticipes = sorted(remboursements_anticipes, 
                                         key=lambda r: r['date'] if isinstance(r['date'], datetime) 
                                                              else datetime.strptime(r['date'], '%Y-%m-%d'))
        
        for remb in remboursements_anticipes:
            date_remb = remb['date'] if isinstance(remb['date'], datetime) else datetime.strptime(remb['date'], '%Y-%m-%d')
            montant_remb = remb['montant']
            
            if montant_remb <= 0:
                continue
                
            penalite = remb.get('penalite', 0) / 100
            montant_penalite = montant_remb * penalite
            montant_effectif = montant_remb - montant_penalite
            type_remb = remb.get('type', 'Partiel')
            
            # Trouver l'index après remboursement
            idx_remb = amortissement[amortissement['date_paiement'] > date_remb].index
            
            if len(idx_remb) > 0:
                idx_remb = idx_remb[0]
                
                # Capital restant avant remboursement
                capital_restant_avant = amortissement.loc[idx_remb - 1, 'capital_restant'] if idx_remb > 0 else amortissement.loc[0, 'capital_restant']
                nouveau_capital = max(0, capital_restant_avant - montant_effectif)
                
                if type_remb == 'Total' and nouveau_capital == 0:
                    # Remboursement total
                    amortissement = amortissement[:idx_remb].copy()
                    if idx_remb > 0:
                        amortissement.loc[idx_remb - 1, 'paiement'] += montant_remb
                else:
                    # Remboursement partiel
                    if idx_remb > 0:
                        amortissement.loc[idx_remb - 1, 'paiement'] += montant_penalite
                    
                    if 'reduction_duree' in type_remb.lower():
                        # Réduction de durée
                        paiement_periodique = amortissement.loc[idx_remb, 'paiement']
                        duree_restante = self._calculer_duree_restante(nouveau_capital, taux_par_periode, paiement_periodique)
                        
                        if duree_restante < len(amortissement) - idx_remb:
                            amortissement = amortissement[:idx_remb + int(duree_restante)].copy()
                    else:
                        # Réduction des mensualités
                        duree_restante = len(amortissement) - idx_remb
                        
                        if taux_par_periode > 0:
                            nouvelle_mensualite = nouveau_capital * (taux_par_periode * (1 + taux_par_periode) ** duree_restante) / \
                                               ((1 + taux_par_periode) ** duree_restante - 1)
                        else:
                            nouvelle_mensualite = nouveau_capital / duree_restante
                        
                        # Vectorisation du recalcul pour les périodes restantes
                        capital_temp = nouveau_capital
                        for j in range(idx_remb, len(amortissement)):
                            interets = capital_temp * taux_par_periode
                            amortissement.loc[j, 'interets'] = interets
                            amortissement.loc[j, 'paiement'] = nouvelle_mensualite
                            amortissement.loc[j, 'principal'] = nouvelle_mensualite - interets
                            capital_temp -= amortissement.loc[j, 'principal']
                            amortissement.loc[j, 'capital_restant'] = capital_temp
        
        return amortissement
    
    def _remplir_dataframe(self, df, amortissement, nom_pret, montant_initial):
        """Remplit le DataFrame principal avec les données du tableau d'amortissement"""
        # Utiliser merge pour éviter les boucles
        cols_to_use = ['date_paiement', 'paiement', 'principal', 'interets', 'capital_restant']
        amort_df = amortissement[cols_to_use].rename(columns={
            'date_paiement': 'date',
            'paiement': f'paiement_{nom_pret}',
            'principal': f'principal_{nom_pret}',
            'interets': f'interets_{nom_pret}',
            'capital_restant': f'capital_restant_{nom_pret}'
        })
        
        # Fusionner avec le DataFrame principal
        df_merged = pd.merge(df, amort_df, on='date', how='left')
        
        # Mettre à jour les colonnes du prêt
        for col in [f'paiement_{nom_pret}', f'principal_{nom_pret}', f'interets_{nom_pret}']:
            df[col] = df_merged[col].fillna(0)
        
        # Interpolation du capital restant
        df[f'capital_restant_{nom_pret}'] = df_merged[f'capital_restant_{nom_pret}'].fillna(montant_initial)
        df[f'capital_restant_{nom_pret}'] = df[f'capital_restant_{nom_pret}'].replace(0, method='ffill')
    
    def _ajouter_frais_pret(self, df, pret, date_debut, nom_pret):
        """Ajoute les frais de prêt au DataFrame"""
        # Frais au premier jour
        frais_premier_jour = (
            pret['frais_dossier_individuel'] +
            pret['frais_courtage_individuel'] +
            pret['frais_divers_pret'] +
            pret['montant'] * pret['frais_caution_individuel'] / 100 +
            pret['montant'] * pret['frais_garantie_hypothecaire'] / 100
        )
        
        # Assurance annuelle
        montant_assurance_annuelle = pret['frais_assurance_individuel']
        
        # Ajout des frais uniques au début du prêt (utiliser loc vectorisé)
        df.loc[df['date'] == date_debut, f'frais_{nom_pret}'] += frais_premier_jour
        
        # Ajout de l'assurance le 31 décembre de chaque année (utiliser loc vectorisé)
        df.loc[(df['date'].dt.month == 12) & (df['date'].dt.day == 31), f'frais_{nom_pret}'] += montant_assurance_annuelle
    
    def _calculer_totaux(self, df):
        """Calcule les totaux pour tous les prêts"""
        # Identifier les colonnes par type
        prefixes = ['paiement_', 'principal_', 'interets_', 'frais_', 'capital_restant_']
        suffix = '_total'
        
        for prefix in prefixes:
            cols = [col for col in df.columns if col.startswith(prefix) and not col.endswith(suffix)]
            if cols:
                df[f'{prefix}total'] = df[cols].sum(axis=1)
    
    def _calculer_duree_restante(self, capital, taux, mensualite):
        """Calcule la durée restante du prêt après un remboursement anticipé"""
        if taux == 0:
            return capital / mensualite
        
        if mensualite <= capital * taux:
            return float('inf')  # Mensualité insuffisante pour couvrir les intérêts
        
        return np.log(mensualite / (mensualite - capital * taux)) / np.log(1 + taux)
    
    def compute_advanced_pret_table(self):
        """Méthode pour des calculs avancés sur les prêts"""
        # À implémenter selon les besoins
        pass