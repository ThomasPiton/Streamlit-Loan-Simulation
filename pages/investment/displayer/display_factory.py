from pages.investment.displayer.display_base import DisplayBase
from pages.investment.displayer.displayer_manager import *

class DisplayFactory(DisplayBase):

    def __init__(self, display:str=None):
        super().__init__()
        self.display = display
    def render(self,**args):
        """_summary_
        """
        if self.display == "DISPLAY_RESULT_BIEN":
            DisplayResultBien(**args).render()
        elif self.display == "DISPLAY_RESULT_V1":
            DisplayResultBien(**args).render()
        elif self.display == "DISPLAY_RESULT_V2":
            DisplayResultBien(**args).render()
        
        
