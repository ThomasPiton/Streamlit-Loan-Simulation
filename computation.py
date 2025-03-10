import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Loan:
    """Classe pour simuler un prêt et générer ses tableaux d'amortissement."""
    
    def __init__(self, montant, taux_interet, duree_annees, differe_mois=0, 
                 assurance_taux=None, assurance_mode="capital initial", 
                 frais_dossier=0, frais_notaire=0, frais_garantie=0):
        """
        Initialise un objet de simulation de prêt.
        
        Args:
            montant (float): Montant du prêt en euros
            taux_interet (float): Taux d'intérêt annuel en pourcentage
            duree_annees (int): Durée du prêt en années
            differe_mois (int): Période de différé en mois (défaut: 0)
            assurance_taux (float): Taux annuel d'assurance en pourcentage (défaut: None)
            assurance_mode (str): Mode de calcul de l'assurance ("capital initial" ou "capital restant dû")
            frais_dossier (float): Frais de dossier en euros
            frais_notaire (float): Frais de notaire en euros
            frais_garantie (float): Frais de garantie en euros
        """
        self.montant = montant
        self.taux_annuel = taux_interet / 100  # Conversion en décimal
        self.taux_mensuel = self.taux_annuel / 12
        self.duree_mois = duree_annees * 12
        self.differe_mois = differe_mois
        
        # Assurance
        self.assurance_taux = assurance_taux / 100 if assurance_taux else None
        self.assurance_mode = assurance_mode
        
        # Frais
        self.frais_dossier = frais_dossier
        self.frais_notaire = frais_notaire
        self.frais_garantie = frais_garantie
        
        # Calcul de la mensualité (formule de l'annuité constante)
        self.mensualite = self._calculer_mensualite()
        
    def _calculer_mensualite(self):
        """Calcule la mensualité de remboursement."""
        if self.taux_mensuel == 0:
            return self.montant / self.duree_mois
        else:
            return self.montant * self.taux_mensuel * (1 + self.taux_mensuel) ** (self.duree_mois - self.differe_mois) / ((1 + self.taux_mensuel) ** (self.duree_mois - self.differe_mois) - 1)
    
    def calculer_assurance_mensuelle(self, capital_restant):
        """Calcule le montant mensuel de l'assurance."""
        if not self.assurance_taux:
            return 0
        
        if self.assurance_mode == "capital initial":
            return self.montant * self.assurance_taux / 12
        else:  # "capital restant dû"
            return capital_restant * self.assurance_taux / 12
    
    def generate_amortization_schedule(self):
        """
        Génère le tableau d'amortissement complet.
        
        Returns:
            pd.DataFrame: Tableau d'amortissement du prêt
        """
        # Initialisation des listes pour stocker les données
        mois = []
        dates = []
        capital_restant = []
        interets = []
        principal = []
        assurance = []
        total_mensualite = []

        # Date de début (aujourd'hui)
        date_actuelle = datetime.now()
        
        capital_du = self.montant
        
        for i in range(1, self.duree_mois + 1):
            mois.append(i)
            date_actuelle = date_actuelle + timedelta(days=30)  # Approximation d'un mois
            dates.append(date_actuelle.strftime("%d/%m/%Y"))
            
            # Calcul de l'assurance
            assurance_mois = self.calculer_assurance_mensuelle(capital_du)
            
            # Pendant la période de différé, on ne rembourse que les intérêts
            if i <= self.differe_mois:
                interet_mois = capital_du * self.taux_mensuel
                principal_mois = 0
                mensualite_totale = interet_mois + assurance_mois
            else:
                interet_mois = capital_du * self.taux_mensuel
                principal_mois = self.mensualite - interet_mois
                mensualite_totale = self.mensualite + assurance_mois
            
            # Mise à jour du capital restant dû
            capital_du = max(0, capital_du - principal_mois)
            
            # Ajout des valeurs aux listes
            capital_restant.append(round(capital_du, 2))
            interets.append(round(interet_mois, 2))
            principal.append(round(principal_mois, 2))
            assurance.append(round(assurance_mois, 2))
            total_mensualite.append(round(mensualite_totale, 2))
        
        # Création du DataFrame
        df = pd.DataFrame({
            "Mois": mois,
            "Date": dates,
            "Intérêts": interets,
            "Principal": principal,
            "Assurance": assurance,
            "Mensualité totale": total_mensualite,
            "Capital restant dû": capital_restant
        })
        
        return df
    
    def calculate_loan_summary(self):
        """
        Calcule les statistiques récapitulatives du prêt.
        
        Returns:
            dict: Dictionnaire contenant les statistiques du prêt
        """
        schedule = self.generate_amortization_schedule()
        
        # Calcul des statistiques
        total_interest = schedule["Intérêts"].sum()
        total_insurance = schedule["Assurance"].sum()
        total_principal = schedule["Principal"].sum()
        total_paid = total_principal + total_interest + total_insurance
        total_cost = total_interest + total_insurance + self.frais_dossier + self.frais_notaire + self.frais_garantie
        cost_percentage = (total_cost / self.montant) * 100
        
        return {
            "Montant emprunté": self.montant,
            "Mensualité": self.mensualite,
            "Durée totale (mois)": self.duree_mois,
            "Durée totale (années)": self.duree_mois / 12,
            "Total intérêts": total_interest,
            "Total assurance": total_insurance,
            "Frais initiaux": self.frais_dossier + self.frais_notaire + self.frais_garantie,
            "Coût total du crédit": total_cost,
            "Total remboursé": total_paid,
            "Coût du crédit (%)": cost_percentage
        }
