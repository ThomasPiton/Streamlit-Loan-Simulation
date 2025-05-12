from models.advanced_simulation.computation.compute_bien import ComputeBien
from models.advanced_simulation.computation.compute_loyer import ComputeLoyer
from models.advanced_simulation.computation.compute_bien import ComputeBien
from models.advanced_simulation.computation.compute_indicateur import ComputeIndicateur
from models.advanced_simulation.computation.compute_pret import ComputePret

# from .compute_charges import ComputeCharges
# from .compute_rentabilite import ComputeRentabilite
# from .compute_cashflow import ComputeCashflow
# from .compute_fiscalite import ComputeFiscalite

class ComputeManager:
    def __init__(self):
        self.calculateurs = [
            ComputePret(),  
            ComputeLoyer(),  
            ComputeBien(), 
            # ComputeCharges(),  
            # ComputeFiscalite(),  
            # ComputeCashflow(),  
            # ComputeRentabilite()
            ComputeIndicateur(),
        ]
        self.resultats = {}  # Maintenant c'est un dict
        
    def run_all(self):
        """Exécute tous les calculateurs dans l'ordre défini"""
        for calculateur in self.calculateurs:
            resultat = calculateur.run()
            # Utiliser le nom de la classe comme clé, ou une propriété .name
            key = type(calculateur).__name__  # Exemple: "ComputeBien"
            self.resultats[key] = resultat
        
        return self.resultats
