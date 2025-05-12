from models.advanced_simulation.displayer.display_base import DisplayBase
from models.advanced_simulation.displayer.displayer_manager import *

class DisplayFactory:
    def __init__(self, display: str = None):
        self.display = display.upper() if display else None  # Toujours en majuscules pour éviter les erreurs

    def render(self):
        """Crée et affiche la bonne visualisation selon la valeur de display."""
        if self.display == "DISPLAY_RESULT_BIEN":
            DisplayResultBien().render()
        
        elif self.display == "DISPLAY_RESULT_V1":
            DisplayPrixEvolutionGraph().render()

        elif self.display == "DISPLAY_RESULT_V2":
            DisplayTimeMetricsGraph().render()

        elif self.display == "DISPLAY_RESULT_V3":
            DisplayUpdateDatesGraph().render()

        elif self.display == "DISPLAY_RESULT_V4":
            DisplayCorrectedPricesGraph().render()

        elif self.display == "DISPLAY_RESULT_V5":
            DisplayImpactOnPriceGraph().render()

        else:
            raise ValueError(f"DisplayFactory: Unknown display type '{self.display}'")
