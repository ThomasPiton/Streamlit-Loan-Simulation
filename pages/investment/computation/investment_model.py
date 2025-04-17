import streamlit as st

from pages.investment.components.input_validator import InputValidator
from pages.investment.components.data_store import DataStore
from pages.investment.computation.compute_manager import ComputeManager

class InvestmentModel:
    def __init__(self):
        self.data = DataStore.get_all()
        self.validator = InputValidator(self.data)
        self.compute_manager = ComputeManager()
        self.resultats = None
        
    def run(self):
        """Exécute le modèle complet et retourne les résultats"""
        # Validation des entrées
        is_valid = self.validator.validate()
        
        # Affichage des warnings
        warnings = self.validator.get_warnings()
        errors = self.validator.get_errors()

        # Affichage des erreurs critiques en premier
        if errors:
            with st.expander(f"❌ {len(errors)} Erreur(s) critique(s)", expanded=False):
                for error in errors:
                    st.error(error)

        # Affichage des warnings ensuite
        if warnings:
            with st.expander(f"⚠️ {len(warnings)} Avertissement(s)", expanded=False):
                for warning in warnings:
                    st.warning(warning)
        
        # Exécution des calculs
        if errors:
            return False
        
        self.resultats = self.compute_manager.run_all()
        return True
        
    def get_resultats(self):
        """Retourne les résultats du modèle"""
        return self.resultats