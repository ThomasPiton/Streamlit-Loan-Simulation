from abc import ABC, abstractmethod
from datetime import date, datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

from pages.investment.components.data_store import DataStore

class BaseCompute(ABC):
    
    def __init__(self):
        self.data = DataStore.all()
        self.prets = self.data["prets"]
        self.loyers = self.data["loyers"]
        self.bien = self.data["bien"]
        self.travaux = self.data["travaux"]
        self.charges = self.data["charges"]
        self.frais_global = self.data["frais_global"]
        self.fisca = self.data["fisca"]
        self.croissance = self.data["croissance"]
        self._get_df_dates()
        self.results = {}  # Pour stocker les résultats de calcul
    
    @abstractmethod  
    def run(self):
        pass
    
    def _get_df_dates(self):
        """ 
        Définit la période d'observation principale :
        - Date de début : minimum entre loyers, prêts, travaux.
        - Date de fin : maximum entre loyers, prêts, travaux, et horizon d'investissement.
        """

        dates_debut = []
        dates_fin = []

        # Dates des loyers
        for loyer in self.loyers:
            dates_debut.append(loyer['start_date']) 
            dates_fin.append(loyer['end_date']) 

        # Dates des prêts
        for pret in self.prets:
            dates_debut.append(pret['start_date'])
            dates_fin.append(pret['start_date'] + relativedelta(months=pret['duree_mois']))
        
        # Dates des travaux
        dates_debut.append(self.travaux['start_date_travaux'])
        dates_fin.append(self.travaux['start_date_travaux'] + relativedelta(months=self.travaux['duree_mois']))
    
        # Date d'horizon d'investissement
        dates_fin.append(min(dates_debut) + relativedelta(years=self.bien['date_horizon']))

        # Calcul du minimum et du maximum
        date_min = min(dates_debut)
        date_max = max(dates_fin)

        # Conversion en datetime si nécessaire
        date_min = datetime.combine(date_min, datetime.min.time())
        date_max = datetime.combine(date_max, datetime.min.time())

        # Créer un DataFrame avec une ligne par jour pour toute la période
        jours = pd.date_range(start=date_min, end=date_max, freq='D')
        self.df_dates = pd.DataFrame({'date': jours})
        
    def get_results(self):
        return self.results