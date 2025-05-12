import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from models.advanced_simulation.component.data_store import DataStore
from models.advanced_simulation.computation.base_compute import BaseCompute

class ComputeLoyer(BaseCompute):
    """
    Classe pour calculer les revenus locatifs basés sur différents contrats de location.
    Permet de gérer plusieurs baux, avec leurs dates de début et de fin, taux d'occupation,
    et possibilité d'indexation.
    """
    
    def __init__(self):
        super().__init__()  
        self.results = {}   # Pour stocker les résultats des calculs
     
    def run(self):
        """
        Crée un DataFrame des revenus locatifs quotidiens pour tous les baux.
        
        Args:
            date_debut_min (datetime, optional): Date de début pour la période de calcul
            date_fin_max (datetime, optional): Date de fin pour la période de calcul
            
        Returns:
            pd.DataFrame: DataFrame avec les revenus locatifs quotidiens
        """

        if not self.loyers:
            return pd.DataFrame(columns=['date', 'loyer_total', 'charges_total'])
        
        self.df_loyers = self.df_dates
        
        # Traiter chaque contrat de location
        for loyer in self.loyers:
            self._calculer_loyer(loyer)
        
        # Calculer Rooling des statistiques agrégées
        self._calculer_statistiques_loyers(loyers)

        return self.df_loyers
    

    def _calculer_loyer(self,loyer):
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
        
        # Création et initialisation des colonnes
        col_loyer = f'loyer_{label}'
        col_charges = f'charges_{label}'
        self.df_loyers[col_loyer] = 0.0
        self.df_loyers[col_charges] = 0.0

        # Calculs journaliers
        loyer_journalier = (loyer_mensuel * 12 / 365) * taux_occupation
        charges_journalieres = (charges_mensuelles * 12 / 365) * taux_occupation

        # Application sur la période active
        mask = (self.df_loyers['date'] >= start_date) & (self.df_loyers['date'] <= end_date)
        self.df_loyers.loc[mask, [f'loyer_{label}', f'charges_{label}']] = loyer_journalier, charges_journalieres

        # Appliquer l'indexation si elle est activée
        if loyer.get('indexation', False):
            self._appliquer_indexation(loyer, col_loyer, col_charges)
        
        # Appliquer la saisonnalité si définie
        if 'mois_occupes' in loyer and loyer['mois_occupes'] < 12:
            self._appliquer_saisonnalite(loyer, col_loyer, col_charges)
        
    def _appliquer_indexation(self, loyer, col_loyer, col_charges):
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
        end_year = self.df_loyers['date'].max().year
        
        for year in range(start_year, end_year + 1):
            date_indexation = datetime(year, date_premiere_indexation.month, date_premiere_indexation.day)
            
            # Vérifier si cette date est dans notre DataFrame
            if date_indexation in self.df_loyers['date'].values:
                # Calculer l'année d'indexation (1ère, 2ème, etc.)
                annee_indexation = year - start_year + 1
                
                # Facteur d'indexation cumulé
                facteur_indexation = (1 + taux_indexation) ** annee_indexation
                
                # Appliquer l'indexation à partir de cette date
                mask_apres_indexation = self.df_loyers['date'] >= date_indexation
                
                # Valeurs de base pour cette période
                base_date_idx = self.df_loyers['date'] == loyer['start_date']
                if any(base_date_idx):
                    valeur_base_loyer = self.df_loyers.loc[base_date_idx, col_loyer].values[0]
                    valeur_base_charges = self.df_loyers.loc[base_date_idx, col_charges].values[0]
                    
                    # Appliquer l'indexation
                    self.df_loyers.loc[mask_apres_indexation, col_loyer] = valeur_base_loyer * facteur_indexation
                    self.df_loyers.loc[mask_apres_indexation, col_charges] = valeur_base_charges * facteur_indexation
        
    
    def _appliquer_saisonnalite(self, loyer, col_loyer, col_charges):
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
            return  # Pas de saisonnalité à appliquer
            
        # Définir les mois d'occupation (par défaut les premiers mois de l'année)
        mois_occupation = loyer.get('mois_occupation', list(range(1, int(mois_occupes) + 1)))
        
        # Appliquer la saisonnalité
        mask_non_occupe = ~self.df_loyers['date'].dt.month.isin(mois_occupation)
        self.df_loyers.loc[mask_non_occupe, col_loyer] = 0
        self.df_loyers.loc[mask_non_occupe, col_charges] = 0
        
        return self.df_loyers
    
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


# Exemple d'utilisation avec les données fournies
if __name__ == "__main__":
    from datetime import date

    # Les loyers fournis
    loyers = [
        {
            'label': 'Loyer 1', 
            'loyer_mensuel': 1000, 
            'charges_mensuelles': 0, 
            'duree_contrat_mois': 36, 
            'duree_contrat_annees': 3, 
            'start_date': date(2025, 4, 25), 
            'end_date': date(2028, 4, 23), 
            'indexation': False, 
            'taux_occupation': 100.0, 
            'mois_occupes': 12.0
        },
        {
            'label': 'Loyer 2', 
            'loyer_mensuel': 1000, 
            'charges_mensuelles': 0, 
            'duree_contrat_mois': 36, 
            'duree_contrat_annees': 3, 
            'start_date': date(2025, 4, 25), 
            'end_date': date(2028, 4, 23), 
            'indexation': False, 
            'taux_occupation': 100.0, 
            'mois_occupes': 12.0
        }
    ]
    
    # Créer l'instance et calculer le DataFrame
    compute_loyer = ComputeLoyer(loyers)
    df_loyers = compute_loyer.run()
    
    # Obtenir les résultats
    resultats = compute_loyer.get_results()
    
    # Afficher un aperçu du DataFrame
    print("Aperçu du DataFrame des loyers quotidiens:")
    print(df_loyers.head())
    
    # Afficher les statistiques annuelles
    print("\nStatistiques annuelles:")
    print(resultats['loyer_annuel'])
    
    # Afficher le total des loyers
    print(f"\nTotal des loyers: {resultats['total_loyers']:.2f} €")
    print(f"Loyer mensuel moyen: {resultats['loyer_mensuel_moyen']:.2f} €")