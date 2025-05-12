import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from models.advanced_simulation.computation.base_compute import BaseCompute

class ComputeBien(BaseCompute):
    """
    Classe pour calculer les revenus locatifs basés sur différents contrats de location.
    Met à jour les prix corrigés à différentes fréquences selon l'inflation et la croissance.
    Les prix restent fixes entre les mises à jour et les taux sont ajustés en fonction de la fréquence.
    """

    def __init__(self):
        super().__init__()
        self.results = {}
        self.prix_initial = self.bien["prix_achat"]
        self.surface = self.bien["surface"]
        
        # Taux annuels
        self.taux_inflation_annuel = self.croissance["taux_inflation"] / 100
        self.taux_growth_annuel = self.croissance["taux_croissance_annuel"] / 100

        # Fréquences de mise à jour séparées pour inflation et croissance
        self.frequence_inflation = self.croissance.get("frequence_taux_inflation", "Annuelle")  # Default: Annuelle
        self.frequence_growth = self.croissance.get("frequence_taux_croissance_annuel", "Annuelle")  # Default: Annuelle

        # Conversion des fréquences en années décimales
        self.frequences = {
            "Annuelle": 1,
            "Semestrielle": 0.5,
            "Trimestrielle": 0.25,
            "Mensuelle": 1 / 12
        }

        self.freq_inflation_annees = self.frequences.get(self.frequence_inflation, 1)
        self.freq_growth_annees = self.frequences.get(self.frequence_growth, 1)
        
        # Ajuster les taux en fonction de la fréquence
        # Formule: (1+taux_annuel)^(fraction_année) - 1
        self.taux_inflation_ajuste = (1 + self.taux_inflation_annuel) ** self.freq_inflation_annees - 1
        self.taux_growth_ajuste = (1 + self.taux_growth_annuel) ** self.freq_growth_annees - 1

    def run(self):
        """
        Crée un DataFrame des revenus locatifs quotidiens pour tous les baux,
        en mettant à jour les prix corrigés uniquement aux dates correspondant aux fréquences définies
        avec des taux ajustés selon la fréquence.
        Entre ces dates, les prix restent fixes.
        """
        df = self.df_dates.copy()

        # Prix de base
        df["prix"] = self.prix_initial
        df["prix_m2"] = self.prix_initial / self.surface

        # Date d'achat
        date_achat = df["date"].min()

        # Temps écoulé en années
        df["annees_ecoulees"] = (df["date"] - date_achat).dt.days / 365.25

        # Identifie les périodes pour les mises à jour
        df["periode_inflation"] = (df["annees_ecoulees"] / self.freq_inflation_annees).astype(int)
        df["periode_growth"] = (df["annees_ecoulees"] / self.freq_growth_annees).astype(int)

        # Création de colonnes pour les mises à jour
        df["derniere_mise_a_jour_inflation"] = df["periode_inflation"] != df["periode_inflation"].shift(1)
        df["derniere_mise_a_jour_growth"] = df["periode_growth"] != df["periode_growth"].shift(1) 
        
        # La première ligne doit toujours être une mise à jour
        df.loc[df.index[0], "derniere_mise_a_jour_inflation"] = True
        df.loc[df.index[0], "derniere_mise_a_jour_growth"] = True

        # Initialisation des prix corrigés
        prix_inflation_courant = self.prix_initial
        prix_growth_courant = self.prix_initial
        
        prixs_corriges_inflation = []
        prixs_corriges_growth = []
        prixs_corriges_total = []

        for i, row in df.iterrows():
            # Mise à jour du prix corrigé par inflation seulement aux dates de changement
            if row["derniere_mise_a_jour_inflation"]:
                # Application du taux d'inflation ajusté par période
                if row["periode_inflation"] > 0:  # On ne fait pas de mise à jour pour la période initiale
                    prix_inflation_courant = prix_inflation_courant * (1 + self.taux_inflation_ajuste)
            
            # Mise à jour du prix corrigé par croissance seulement aux dates de changement
            if row["derniere_mise_a_jour_growth"]:
                # Application du taux de croissance ajusté par période
                if row["periode_growth"] > 0:  # On ne fait pas de mise à jour pour la période initiale
                    prix_growth_courant = prix_growth_courant * (1 + self.taux_growth_ajuste)
            
            # Stockage des prix dans les listes
            prixs_corriges_inflation.append(prix_inflation_courant)
            prixs_corriges_growth.append(prix_growth_courant)
            
            # Prix total combinant les effets d'inflation et de croissance
            prix_total = prix_inflation_courant * prix_growth_courant / self.prix_initial
            prixs_corriges_total.append(prix_total)

        # Ajout des résultats au DataFrame
        df["prix_corrige_inflation"] = prixs_corriges_inflation
        df["prix_corrige_growth"] = prixs_corriges_growth
        df["prix_corrige_total"] = prixs_corriges_total

        # Calcul des impacts
        df["impact_prix_total"] = df["prix_corrige_total"] - df["prix"]
        df["impact_prix_m2_total"] = df["prix_corrige_total"] / self.surface - df["prix_m2"]

        return df