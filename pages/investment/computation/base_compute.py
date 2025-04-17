from abc import ABC, abstractmethod
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
        self.results = {}  # Pour stocker les résultats de calcul
        
    def run(self):
        pass
        
    def get_results(self):
        return self.results