from abc import ABC, abstractmethod

class BaseSection(ABC):
    def __init__(self):
        # Tu peux y stocker des données partagées ou initialiser des états
        pass

    @abstractmethod
    def render(self):
        """
        Méthode à implémenter dans chaque section pour afficher les composants Streamlit.
        """
        pass