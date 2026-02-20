from ib_async import *
from .base import BrokerBase
import pandas as pd

class IBKRBroker(BrokerBase):
    def __init__(self, config):
        super().__init__(config)
        self.ib = IB()
        self.ib.connect(config["broker"]["ib_host"], config["broker"]["ib_port"], clientId=config["broker"]["ib_client_id"])

    async def get_bars(self, symbol, interval, limit=500):
        contract = Stock(symbol, "SMART", "USD")
        bars = await self.ib.reqHistoricalDataAsync(
            contract, endDateTime="", durationStr=f"{limit} D",
            barSizeSetting=interval.replace("Min", " mins").replace("Hour", " hours"),
            whatToShow="TRADES", useRTH=True
        )
        df = util.df(bars)
        df = df.rename(columns={"date": "timestamp", "open": "open", "high": "high", "low": "low", "close": "close", "volume": "volume"})
        return df

    async def place_order(self, symbol, side, qty):
        contract = Stock(symbol, "SMART", "USD")
        order = MarketOrder(side.upper(), qty)
        self.ib.placeOrder(contract, order)

    async def get_account(self):
        return self.ib.accountSummary()
