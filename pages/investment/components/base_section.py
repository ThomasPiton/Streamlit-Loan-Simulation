from abc import ABC, abstractmethod

class BaseSection(ABC):
    
    def __init__(self):
        pass

    @abstractmethod
    def render(self):
        """
        Méthode à implémenter dans chaque section pour afficher les composants Streamlit.
        """
        pass