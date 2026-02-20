from alpaca.trading.client import TradingClient
from alpaca.data import StockHistoricalDataClient, TimeFrame, StockBarsRequest
from .base import BrokerBase
import pandas as pd

class AlpacaBroker(BrokerBase):
    def __init__(self, config):
        super().__init__(config)
        key = config["broker"]["alpaca_api_key"]
        secret = config["broker"]["alpaca_secret_key"]
        self.trading = TradingClient(key, secret, paper=self.paper)
        self.data = StockHistoricalDataClient(key, secret)

    async def get_bars(self, symbol, interval, limit=500):
        tf = {"1Min": TimeFrame.Minute, "5Min": TimeFrame.FiveMinute,
              "15Min": TimeFrame.FifteenMinute, "1Hour": TimeFrame.Hour}.get(interval, TimeFrame.Minute)
        req = StockBarsRequest(symbol_or_symbols=symbol, timeframe=tf, limit=limit)
        bars = self.data.get_stock_bars(req).df
        return bars.reset_index()

    async def place_order(self, symbol, side, qty):
        side = "buy" if side.upper() == "BUY" else "sell"
        self.trading.submit_order(symbol=symbol, qty=qty, side=side, type="market", time_in_force="gtc")
        print(f"✅ {side.upper()} {qty} {symbol} placed")

    async def get_account(self):
        return self.trading.get_account()
