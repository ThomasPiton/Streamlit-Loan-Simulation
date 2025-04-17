import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from pages.investment.components.data_store import DataStore
from pages.investment.computation.base_compute import BaseCompute

class ComputeLoyer(BaseCompute):
    """
    Classe pour calculer les revenus locatifs basés sur différents contrats de location.
    Permet de gérer plusieurs baux, avec leurs dates de début et de fin, taux d'occupation,
    et possibilité d'indexation.
    """
    
    def __init__(self):
        super().__init__()  # Appelle le constructeur parent pour initialiser les données
        self.results = {}   # Pour stocker les résultats des calculs
     
    def run(self):
        """
        Exécute le calcul complet des revenus locatifs.
        Cette méthode est appelée par la classe InvestmentModel.
        
        Returns:
            dict: Résultats des calculs
        """
        df_loyers = self.compute_loyers_table()
        
        # Calculs supplémentaires si nécessaire
        
        return self.results
    
    def compute_loyers_table(self, loyers=None, date_debut_min=None, date_fin_max=None):
        """
        Crée un DataFrame des revenus locatifs quotidiens pour tous les baux.
        
        Args:
            loyers (list): Liste de dictionnaires contenant les informations des baux
            date_debut_min (datetime): Date de début pour la période de calcul
            date_fin_max (datetime): Date de fin pour la période de calcul
            
        Returns:
            pd.DataFrame: DataFrame avec les revenus locatifs quotidiens
        """
        # Utiliser les loyers passés en paramètre ou ceux stockés dans la classe
        loyers = loyers if loyers is not None else self.loyers
        
        if not loyers:
            return pd.DataFrame(columns=['date', 'loyer_total', 'charges_total'])
        
        # Convertir les dates string en datetime si nécessaire
        loyers = self._normaliser_dates_loyers(loyers)
        
        # Déterminer les dates de début et de fin
        if date_debut_min is None:
            date_debut_min = min(loyer['start_date'] for loyer in loyers 
                                if isinstance(loyer['start_date'], (date, datetime)))
            # Conversion en datetime si c'est un objet date
            if isinstance(date_debut_min, date) and not isinstance(date_debut_min, datetime):
                date_debut_min = datetime.combine(date_debut_min, datetime.min.time())
        
        if date_fin_max is None:
            date_fin_max = max(loyer['end_date'] for loyer in loyers 
                              if isinstance(loyer['end_date'], (date, datetime)))
            # Conversion en datetime si c'est un objet date
            if isinstance(date_fin_max, date) and not isinstance(date_fin_max, datetime):
                date_fin_max = datetime.combine(date_fin_max, datetime.min.time())
        
        # Créer un DataFrame avec une ligne par jour pour toute la période
        jours = pd.date_range(start=date_debut_min, end=date_fin_max, freq='D')
        df = pd.DataFrame({'date': jours})
        
        # Initialiser les colonnes totales
        df['loyer_total'] = 0.0
        df['charges_total'] = 0.0
        
        # Traiter chaque contrat de location
        for i, loyer in enumerate(loyers):
            df = self._ajouter_loyer_au_dataframe(df, loyer)
        
        # Calculer des statistiques agrégées
        self._calculer_statistiques_loyers(df, loyers)
        
        return df
    
    def _normaliser_dates_loyers(self, loyers):
        """
        Normalise les dates dans les objets loyer pour assurer la compatibilité.
        Convertit les chaînes de caractères en objets datetime.
        """
        for i, loyer in enumerate(loyers):
            # Copier pour éviter de modifier l'original
            loyers[i] = loyer.copy()
            
            # Normaliser start_date
            if isinstance(loyer.get('start_date'), str):
                loyers[i]['start_date'] = datetime.strptime(loyer['start_date'], '%Y-%m-%d')
            elif isinstance(loyer.get('start_date'), date) and not isinstance(loyer.get('start_date'), datetime):
                loyers[i]['start_date'] = datetime.combine(loyer['start_date'], datetime.min.time())
                
            # Normaliser end_date
            if isinstance(loyer.get('end_date'), str):
                loyers[i]['end_date'] = datetime.strptime(loyer['end_date'], '%Y-%m-%d')
            elif isinstance(loyer.get('end_date'), date) and not isinstance(loyer.get('end_date'), datetime):
                loyers[i]['end_date'] = datetime.combine(loyer['end_date'], datetime.min.time())
                
            # Si end_date n'est pas défini, le calculer à partir de la durée
            if 'end_date' not in loyers[i] or loyers[i]['end_date'] is None:
                duree_mois = loyers[i].get('duree_contrat_mois', 0) or loyers[i].get('duree_contrat_annees', 0) * 12
                if duree_mois > 0 and 'start_date' in loyers[i]:
                    loyers[i]['end_date'] = loyers[i]['start_date'] + relativedelta(months=duree_mois)
        
        return loyers
    
    def _ajouter_loyer_au_dataframe(self, df, loyer):
        """
        Ajoute un contrat de location au DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame des revenus locatifs
            loyer (dict): Informations sur le contrat de location
            
        Returns:
            pd.DataFrame: DataFrame mis à jour
        """
        label = loyer.get('label', f"Loyer_{loyer.get('id', '')}")
        loyer_mensuel = loyer.get('loyer_mensuel', 0)
        charges_mensuelles = loyer.get('charges_mensuelles', 0)
        taux_occupation = loyer.get('taux_occupation', 100) / 100  # Conversion en décimal
        start_date = loyer.get('start_date')
        end_date = loyer.get('end_date')
        
        # Création de colonnes spécifiques pour ce bail
        col_loyer = f'loyer_{label}'
        col_charges = f'charges_{label}'
        
        # Initialiser les colonnes à 0
        df[col_loyer] = 0.0
        df[col_charges] = 0.0
        
        # Calculer le loyer journalier (en tenant compte du taux d'occupation)
        loyer_journalier = (loyer_mensuel * 12 / 365) * taux_occupation
        charges_journalieres = (charges_mensuelles * 12 / 365) * taux_occupation
        
        # Appliquer les valeurs pour les jours où le bail est actif
        mask_actif = (df['date'] >= start_date) & (df['date'] <= end_date)
        df.loc[mask_actif, col_loyer] = loyer_journalier
        df.loc[mask_actif, col_charges] = charges_journalieres
        
        # Appliquer l'indexation si elle est activée
        if loyer.get('indexation', False):
            df = self._appliquer_indexation(df, loyer, col_loyer, col_charges)
        
        # Appliquer la saisonnalité si définie
        if 'mois_occupes' in loyer and loyer['mois_occupes'] < 12:
            df = self._appliquer_saisonnalite(df, loyer, col_loyer, col_charges)
        
        # Ajouter au total
        df['loyer_total'] += df[col_loyer]
        df['charges_total'] += df[col_charges]
        
        return df
    
    def _appliquer_indexation(self, df, loyer, col_loyer, col_charges):
        """
        Applique l'indexation annuelle aux loyers et charges.
        
        Args:
            df (pd.DataFrame): DataFrame des revenus locatifs
            loyer (dict): Informations sur le contrat de location
            col_loyer (str): Nom de la colonne des loyers
            col_charges (str): Nom de la colonne des charges
            
        Returns:
            pd.DataFrame: DataFrame avec indexation appliquée
        """
        # Taux d'indexation (par défaut IRL = 2%)
        taux_indexation = loyer.get('taux_indexation', 2) / 100
        date_premiere_indexation = loyer.get('date_premiere_indexation')
        
        # Si la date de première indexation n'est pas définie, utiliser la date de début + 1 an
        if date_premiere_indexation is None:
            date_premiere_indexation = loyer['start_date'] + relativedelta(years=1)
        
        # Déterminer toutes les dates d'indexation (chaque année)
        start_year = date_premiere_indexation.year
        end_year = df['date'].max().year
        
        for year in range(start_year, end_year + 1):
            date_indexation = datetime(year, date_premiere_indexation.month, date_premiere_indexation.day)
            
            # Vérifier si cette date est dans notre DataFrame
            if date_indexation in df['date'].values:
                # Calculer l'année d'indexation (1ère, 2ème, etc.)
                annee_indexation = year - start_year + 1
                
                # Facteur d'indexation cumulé
                facteur_indexation = (1 + taux_indexation) ** annee_indexation
                
                # Appliquer l'indexation à partir de cette date
                mask_apres_indexation = df['date'] >= date_indexation
                
                # Valeurs de base pour cette période
                valeur_base_loyer = df.loc[df['date'] == loyer['start_date'], col_loyer].values[0]
                valeur_base_charges = df.loc[df['date'] == loyer['start_date'], col_charges].values[0]
                
                # Appliquer l'indexation
                df.loc[mask_apres_indexation, col_loyer] = valeur_base_loyer * facteur_indexation
                df.loc[mask_apres_indexation, col_charges] = valeur_base_charges * facteur_indexation
        
        return df
    
    def _appliquer_saisonnalite(self, df, loyer, col_loyer, col_charges):
        """
        Applique la saisonnalité au contrat de location.
        Ajuste les loyers en fonction du nombre de mois occupés par an.
        
        Args:
            df (pd.DataFrame): DataFrame des revenus locatifs
            loyer (dict): Informations sur le contrat de location
            col_loyer (str): Nom de la colonne des loyers
            col_charges (str): Nom de la colonne des charges
            
        Returns:
            pd.DataFrame: DataFrame avec saisonnalité appliquée
        """
        mois_occupes = loyer.get('mois_occupes', 12)
        
        if mois_occupes >= 12:
            return df  # Pas de saisonnalité à appliquer
            
        # Définir les mois d'occupation (par défaut les premiers mois de l'année)
        mois_occupation = loyer.get('mois_occupation', list(range(1, int(mois_occupes) + 1)))
        
        # Appliquer la saisonnalité
        mask_non_occupe = ~df['date'].dt.month.isin(mois_occupation)
        df.loc[mask_non_occupe, col_loyer] = 0
        df.loc[mask_non_occupe, col_charges] = 0
        
        return df
    
    def _calculer_statistiques_loyers(self, df, loyers):
        """
        Calcule diverses statistiques sur les revenus locatifs et les stocke dans self.results.
        
        Args:
            df (pd.DataFrame): DataFrame des revenus locatifs
            loyers (list): Liste des contrats de location
        """
        # Calculs annuels
        df_annuel = df.copy()
        df_annuel['year'] = df_annuel['date'].dt.year
        stats_annuelles = df_annuel.groupby('year').agg({
            'loyer_total': 'sum',
            'charges_total': 'sum'
        }).reset_index()
        
        # Calculs mensuels
        df_mensuel = df.copy()
        df_mensuel['year_month'] = df_mensuel['date'].dt.strftime('%Y-%m')
        stats_mensuelles = df_mensuel.groupby('year_month').agg({
            'loyer_total': 'sum',
            'charges_total': 'sum'
        }).reset_index()
        
        # Résumé global
        total_loyers = df['loyer_total'].sum()
        total_charges = df['charges_total'].sum()
        duree_jours = len(df)
        
        # Moyenne mensuelle
        loyer_mensuel_moyen = total_loyers / (duree_jours / 30.4375)  # Moyenne de jours par mois
        charges_mensuelles_moyennes = total_charges / (duree_jours / 30.4375)
        
        # Stockage des résultats
        self.results.update({
            'loyer_quotidien': df,
            'loyer_annuel': stats_annuelles,
            'loyer_mensuel': stats_mensuelles,
            'total_loyers': total_loyers,
            'total_charges': total_charges,
            'loyer_mensuel_moyen': loyer_mensuel_moyen,
            'charges_mensuelles_moyennes': charges_mensuelles_moyennes,
            'duree_jours': duree_jours,
            'nb_baux': len(loyers)
        })
        
        # Statistiques par bail
        stats_par_bail = []
        for loyer in loyers:
            label = loyer.get('label', f"Loyer_{loyer.get('id', '')}")
            col_loyer = f'loyer_{label}'
            col_charges = f'charges_{label}'
            
            if col_loyer in df.columns:
                stats_bail = {
                    'label': label,
                    'loyer_total': df[col_loyer].sum(),
                    'charges_total': df[col_charges].sum() if col_charges in df.columns else 0,
                    'debut': loyer.get('start_date'),
                    'fin': loyer.get('end_date'),
                    'duree_mois': loyer.get('duree_contrat_mois', 0),
                    'taux_occupation': loyer.get('taux_occupation', 100)
                }
                stats_par_bail.append(stats_bail)
        
        self.results['stats_par_bail'] = stats_par_bail
        
        return self.results

    def get_results(self):
        """
        Retourne les résultats des calculs.
        
        Returns:
            dict: Résultats des calculs
        """
        return self.results