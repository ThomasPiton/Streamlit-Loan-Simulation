from models.pret_zero.config import *
import pandas as pd
from typing import Dict, Tuple, List, Optional
class ComputePretZero:
    
    def __init__(self, zone_location: str, nb_occupants: int, nature_bien: str, 
                 proprietaire_2ans: bool, prix_achat: float, revenus: float, 
                 duree_pret: int, duree_differe: int):
        """
        Initialise le calculateur PTZ
        
        Args:
            zone_location: Zone géographique (A/A bis, B1, B2, C)
            nb_occupants: Nombre d'occupants du logement
            nature_bien: Type de bien ('neuf' ou 'ancien')
            proprietaire_2ans: True si propriétaire dans les 2 dernières années
            prix_achat: Prix d'achat du bien en euros
            revenus: Revenus totaux du foyer en euros
            duree_pret: Durée souhaitée du prêt en années
            duree_differe: Durée du différé en années
        """
        self.zone_location = zone_location 
        self.nb_occupants = int(nb_occupants)
        self.nature_bien = nature_bien
        self.proprietaire_2ans = proprietaire_2ans
        self.prix_achat = float(prix_achat)
        self.revenus = float(revenus)
        self.duree_pret = int(duree_pret)
        self.duree_differe = int(duree_differe)
        
        # Initialize calculated attributes
        self.eligible = {"eligible": True, "raisons": []}
        self.tranche = None
        self.plafond_revenus = None
        self.revenus_ajustes = None
        self.montant_ptz = 0
        self.quotite = 0
        self.coefficient_familial = None
        self.montant_max_zone = 0
        self.montant_base = 0
        self.capital_differe = 0
        self.periode_differe = 0
        self.mensualite = 0
        self.annuite = 0
        self.tableau = []

    def run(self) -> Dict:
        """
        Lance tous les calculs et retourne un résumé complet
        
        Returns:
            Dict contenant tous les résultats calculés
        """
        self._check_eligible()
        
        if self.eligible["eligible"]:
            self._generer_tableau_amortissement()
        
        return {
            "eligibilite": {
                "eligible": self.eligible["eligible"],
                "raisons_ineligibilite": self.eligible["raisons"]
            },
            "revenus": {
                "revenus_total": self.revenus,
                "tranche_revenus": self.tranche,
                "plafond_revenus": self.plafond_revenus
            },
            "ptz": {
                "montant_ptz": self.montant_ptz,
                "quotite": self.quotite,
                "coefficient_familial": self.coefficient_familial,
                "montant_base": self.montant_base or 0
            },
            "capital_differe": {
                "montant_differe": self.capital_differe,
                "periode_differe_annees": self.periode_differe,
                "mensualite": self.mensualite,
                "annuite": self.annuite
            },
            "tableau_amortissement": self.tableau
        }   

    def _check_eligible(self) -> None:
        """Vérifie l'éligibilité et calcule les paramètres de base"""
        
        # Limite à 8 personnes pour le barème
        nb_occupants = min(self.nb_occupants, 8)
        self.coefficient_familial = COEFFICIENT_FAMILIAL[nb_occupants]
        self.plafond_revenus = PLAFONDS_REVENUS[nb_occupants][self.zone_location]

        # Calcul du revenu ajusté selon le coefficient familial
        self.revenus_ajustes = self.revenus / self.coefficient_familial
        
        # Vérifications d'éligibilité
        self.eligible = {"eligible": True, "raisons": []}
        
        # Vérification propriétaire dans les 2 dernières années
        if self.proprietaire_2ans:
            self.eligible["eligible"] = False
            self.eligible["raisons"].append("Vous avez été propriétaire de votre résidence principale dans les 2 dernières années")
        
        # Vérification zone pour logement ancien
        if self.nature_bien == "ancien" and self.zone_location not in ['B2', 'C']:
            self.eligible["eligible"] = False
            self.eligible["raisons"].append(f"L'acquisition d'un logement ancien n'est pas éligible en zone {self.zone_location}")
        
        # Détermination de la tranche de revenus
        self._determine_tranche()
        
        # Si pas de tranche déterminée, arrêter ici
        if self.tranche is None:
            return
        
        # Vérification durée différé vs tranche 
        if self.duree_differe > BAREME_REMBOURSEMENT[self.tranche]['duree_periode1']:
            self.eligible["eligible"] = False
            self.eligible["raisons"].append(f"En raison de vos revenus, vous appartenez à la tranche {self.tranche} et donc vous dépassez le différé maximum de cette tranche fixé à {BAREME_REMBOURSEMENT[self.tranche]['duree_periode1']} ans.")
        
        # Vérification tranche 4, ne pas faire de différé
        if self.tranche == 4 and self.duree_differe > 0:
            self.eligible["eligible"] = False
            self.eligible["raisons"].append("La tranche 4 ne peut pas réaliser de différé.")
        
        # Vérification tranche 4, durée maximum 10 ans
        if self.tranche == 4 and self.duree_pret > 10:
            self.eligible["eligible"] = False
            self.eligible["raisons"].append("La tranche 4 ne peut pas réaliser de prêt pour une durée supérieure à 10 ans.")
        
        # Si éligible, calculer le montant PTZ
        if self.eligible["eligible"]:
            self._calculer_montant_ptz()
        
    def _determine_tranche(self) -> None:
        """Détermine la tranche de revenus selon les plafonds et le coefficient familial"""

        # Détermination de la tranche en fonction des ressources ajustées
        for tranche, plafonds_zone in TRANCHES_RESSOURCES.items():
            plafond_zone = plafonds_zone[self.zone_location]
            if self.revenus_ajustes <= plafond_zone:
                self.tranche = tranche
                return

        # Si aucune tranche n'est trouvée : non éligible
        self.eligible["eligible"] = False
        self.eligible["raisons"].append(
            f"Votre revenu considéré est de {self.revenus} avec un coefficient familial de {self.coefficient_familial}, "
            f"ce qui vous amène à un revenu ajusté de {self.revenus_ajustes:.2f}. "
            f"Ce revenu ajusté dépasse le plafond maximal de la zone {self.zone_location} pour la tranche 4, "
            f"qui est de {TRANCHES_RESSOURCES[4][self.zone_location]}."
        )

    def _calculer_montant_ptz(self) -> None:
        """Calcule le montant du PTZ selon les règles"""
        
        # Détermination du nombre de personnes retenu (maximum 5 dans le barème)
        nbr_occupants_retenus = min(self.nb_occupants, 5)
        self.montant_max_zone = PLAFOND_OPERATION[nbr_occupants_retenus][self.zone_location]
        
        # Calcul de la quotité selon la tranche
        self.quotite = QUOTITES[self.tranche][self.nature_bien]
        
        # Calcul du montant du PTZ en appliquant la quotité au minimum entre le prix d'achat et le plafond de la zone
        self.montant_base = min(self.prix_achat, self.montant_max_zone)
        self.montant_ptz = self.montant_base * (self.quotite / 100)

    def _generer_tableau_amortissement(self) -> None:
        """
        Génère le tableau d'amortissement basé sur:
        - duree_pret: durée totale du prêt
        - duree_differe: durée du différé
        - montant_ptz: montant total à rembourser
        """
        
        # Calcul de la durée de remboursement effective
        duree_remboursement = self.duree_pret - self.duree_differe
        self.periode_differe = self.duree_differe
        
        # Calcul de la mensualité et de l'annuité
        if duree_remboursement > 0:
            self.mensualite = self.montant_ptz / (duree_remboursement * 12)
            self.annuite = self.montant_ptz / duree_remboursement
        else:
            self.mensualite = 0
            self.annuite = 0
        
        # Génération du tableau d'amortissement
        tableau = []
        capital_restant = self.montant_ptz
        capital_rembourse_cumule = 0
        
        for annee in range(1, self.duree_pret + 1):
            # Déterminer si on est en période de différé ou de remboursement
            if annee <= self.duree_differe:
                # Période de différé - pas de remboursement
                mensualite_courante = 0
                remboursement_annuel = 0
                periode_nom = "Différé"
            else:
                # Période de remboursement
                mensualite_courante = self.mensualite
                remboursement_annuel = min(self.annuite, capital_restant)
                periode_nom = "Remboursement"
            
            # Générer les lignes mensuelles pour l'année
            capital_restant_debut_annee = capital_restant
            
            for mois in range(1, 13):
                mois_absolu = (annee - 1) * 12 + mois
                
                if remboursement_annuel > 0:
                    remboursement_mensuel = remboursement_annuel / 12
                else:
                    remboursement_mensuel = 0
                
                capital_restant_debut_mois = capital_restant_debut_annee - ((mois - 1) * remboursement_mensuel)
                capital_restant_fin_mois = max(0, capital_restant_debut_mois - remboursement_mensuel)
                
                capital_rembourse_cumule += remboursement_mensuel
                
                tableau.append({
                    'Mois': mois_absolu,
                    'Année': annee,
                    'Période': periode_nom,
                    'Capital restant début': round(capital_restant_debut_mois, 2),
                    'Remboursement capital': round(remboursement_mensuel, 2),
                    'Capital rembourse cumulé': round(capital_rembourse_cumule, 2),
                    'Intérêts': 0.0,  # PTZ sans intérêts
                    'Mensualité': round(mensualite_courante, 2),
                    'Capital restant fin': round(capital_restant_fin_mois, 2)
                })
                
                # Arrêter si tout est remboursé
                if capital_restant_fin_mois <= 0:
                    break
            
            # Mettre à jour le capital restant pour l'année suivante
            capital_restant -= remboursement_annuel
            
            # Arrêter si tout est remboursé
            if capital_restant <= 0:
                break
        
        self.tableau = pd.DataFrame(tableau)