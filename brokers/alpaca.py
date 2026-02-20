import os
from dotenv import load_dotenv

from alpaca.trading.client import TradingClient
from alpaca.data import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.requests import StockBarsRequest

from .base import BrokerBase
import pandas as pd

# Load .env (safe to call multiple times)
load_dotenv()

class AlpacaBroker(BrokerBase):
    def __init__(self, config):
        super().__init__(config)
        
        # Get keys: prefer .env, fallback to config.yaml
        key = (
            os.getenv("ALPACA_API_KEY") or
            config["broker"].get("alpaca_api_key", "")
        )
        secret = (
            os.getenv("ALPACA_SECRET_KEY") or
            config["broker"].get("alpaca_secret_key", "")
        )
        
        if not key or not secret:
            raise ValueError(
                "Alpaca API key and/or secret not found. "
                "Set them in .env file or in config.yaml under broker section."
            )
        
        self.trading = TradingClient(key, secret, paper=self.paper)
        self.data = StockHistoricalDataClient(key, secret)

    async def get_bars(self, symbol: str, interval: str, limit: int = 500) -> pd.DataFrame:
        """
        Fetch historical bars using current alpaca-py timeframe syntax.
        """
        # Modern timeframe creation (compatible with 0.20+)
        timeframe_map = {
            "1Min":  TimeFrame(1, TimeFrameUnit.Minute),
            "5Min":  TimeFrame(5, TimeFrameUnit.Minute),
            "15Min": TimeFrame(15, TimeFrameUnit.Minute),
            "1Hour": TimeFrame(1, TimeFrameUnit.Hour),
            # Add more as needed
            # "1Day":  TimeFrame(1, TimeFrameUnit.Day),
        }
        
        tf = timeframe_map.get(interval)
        if tf is None:
            raise ValueError(
                f"Unsupported interval '{interval}'. "
                f"Supported: {list(timeframe_map.keys())}"
            )
        
        req = StockBarsRequest(
            symbol_or_symbols = symbol,
            timeframe        = tf,
            limit            = limit
        )
        
        bars = self.data.get_stock_bars(req).df
        
        # Reset index to make timestamp a column
        return bars.reset_index()

    async def place_order(self, symbol: str, side: str, qty: float):
        side_str = "buy" if side.upper() == "BUY" else "sell"
        self.trading.submit_order(
            symbol        = symbol,
            qty           = qty,
            side          = side_str,
            type          = "market",
            time_in_force = "gtc"
        )
        print(f"Placed {side_str.upper()} order for {qty} {symbol}")

    async def get_account(self):
        return self.trading.get_account()
