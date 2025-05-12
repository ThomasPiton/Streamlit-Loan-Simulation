from abc import ABC, abstractmethod
from datetime import date, datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

from models.advanced_simulation.component.data_store import DataStore

class DisplayBase(ABC):
    
    def __init__(self):
        self.data = DataStore.all()
        self.result = self.data["resultats"]

    @abstractmethod  
    def render(self):
        pass