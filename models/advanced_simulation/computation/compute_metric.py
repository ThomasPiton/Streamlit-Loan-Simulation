import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from models.advanced_simulation.computation.base_compute import BaseCompute

class ComputeMetric(BaseCompute):
    """
    Classe pour calculer les revenus locatifs basés sur différents contrats de location.
    Met à jour les prix corrigés à différentes fréquences selon l'inflation et la croissance.
    Les prix restent fixes entre les mises à jour et les taux sont ajustés en fonction de la fréquence.
    """

    def __init__(self):
        super().__init__()
        self.results = {}
        self.prix_initial = self.bien["prix_achat"]
        self.loyers

    def run(self):
        """
        Crée un DataFrame des revenus locatifs quotidiens pour tous les baux,
        en mettant à jour les prix corrigés uniquement aux dates correspondant aux fréquences définies
        avec des taux ajustés selon la fréquence.
        Entre ces dates, les prix restent fixes.
        """
        df = self.df_dates.copy()
        df["prix"] = self.prix_initial


        return df