from abc import ABC, abstractmethod
import pandas as pd

class StrategyBase(ABC):
    def __init__(self, config):
        self.name = config["name"]
        self.symbols = config["symbols"]
        self.interval = config["interval"]
        self.params = config.get("params", {})

    @abstractmethod
    def generate_signal(self, df: pd.DataFrame, params: dict) -> str:
        pass
