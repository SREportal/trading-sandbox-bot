import robin_stocks.robinhood as rh
from .base import BrokerBase
import pandas as pd
import warnings

warnings.warn("Robinhood stock trading is unofficial – use only for crypto learning", UserWarning)

class RobinhoodBroker(BrokerBase):
    def __init__(self, config):
        super().__init__(config)
        rh.login(config["broker"]["rh_username"], config["broker"]["rh_password"])

    async def get_bars(self, symbol, interval, limit=500):
        # Robinhood historical is limited – use for demo only
        df = pd.DataFrame()  # placeholder – replace with real call if needed
        return df

    async def place_order(self, symbol, side, qty):
        print("Robinhood order (demo only):", side, qty, symbol)

    async def get_account(self):
        return {"equity": 10000}
