from pages.investment.computation.compute_pret import ComputePret
from pages.investment.computation.compute_loyer import ComputeLoyer
# from .compute_charges import ComputeCharges
# from .compute_rentabilite import ComputeRentabilite
# from .compute_cashflow import ComputeCashflow
# from .compute_fiscalite import ComputeFiscalite

class ComputeManager:
    def __init__(self):
        self.calculateurs = [
            ComputePret(),  # Calcul des échéances de prêt
            ComputeLoyer(),  # Calcul des revenus locatifs
            # ComputeCharges(),  # Calcul des charges
            # ComputeFiscalite(),  # Calcul de la fiscalité
            # ComputeCashflow(),  # Calcul des flux de trésorerie
            # ComputeRentabilite()  # Calcul des indicateurs de rentabilité
        ]
        self.resultats = {}
    
    def run_all(self):
        """Exécute tous les calculateurs dans l'ordre défini"""
        for calculateur in self.calculateurs:
            calculateur.run()
            self.resultats.update(calculateur.get_results())
        
        return self.resultats