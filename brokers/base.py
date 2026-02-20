from abc import ABC, abstractmethod
import pandas as pd

class BrokerBase(ABC):
    def __init__(self, config):
        self.config = config
        self.paper = config["mode"] == "paper"

    @abstractmethod
    async def get_bars(self, symbol: str, interval: str, limit: int = 500) -> pd.DataFrame:
        pass

    @abstractmethod
    async def place_order(self, symbol: str, side: str, qty: float):
        pass

    @abstractmethod
    async def get_account(self):
        pass
