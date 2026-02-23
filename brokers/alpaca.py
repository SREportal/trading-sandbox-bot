# brokers/alpaca.py
import os
from dotenv import load_dotenv

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.data import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.requests import StockBarsRequest

from .base import BrokerBase
import pandas as pd

# Load .env (safe even if already loaded)
load_dotenv()

class AlpacaBroker(BrokerBase):
    def __init__(self, config):
        super().__init__(config)

        # Get credentials: prefer .env → fallback to config.yaml
        key = os.getenv("ALPACA_API_KEY") or config["broker"].get("alpaca_api_key", "")
        secret = os.getenv("ALPACA_SECRET_KEY") or config["broker"].get("alpaca_secret_key", "")

        if not key or not secret:
            raise ValueError("Alpaca API key and/or secret missing. Set in .env or config.yaml.")

        print(f"[AlpacaBroker] Using key: {key[:6]}... (len={len(key)}) | paper={self.paper}")

        self.trading = TradingClient(key, secret, paper=self.paper)
        self.data    = StockHistoricalDataClient(key, secret)

    async def get_bars(self, symbol: str, interval: str, limit: int = 500) -> pd.DataFrame:
        timeframe_map = {
            "1Min":  TimeFrame(1,  TimeFrameUnit.Minute),
            "5Min":  TimeFrame(5,  TimeFrameUnit.Minute),
            "15Min": TimeFrame(15, TimeFrameUnit.Minute),
            "1Hour": TimeFrame(1,  TimeFrameUnit.Hour),
            "1Day":  TimeFrame(1,  TimeFrameUnit.Day),
        }

        tf = timeframe_map.get(interval)
        if tf is None:
            raise ValueError(f"Unsupported interval '{interval}'. Supported: {list(timeframe_map.keys())}")

        req = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=tf,
            limit=limit
        )

        bars = self.data.get_stock_bars(req).df
        return bars.reset_index()

    async def place_order(self, symbol: str, side: str, qty: float):
        side_str = "buy" if side.upper() == "BUY" else "sell"

        order_data = MarketOrderRequest(
            symbol       = symbol,
            qty          = qty,
            side         = side_str,
            time_in_force = "gtc"
        )

        try:
            order = self.trading.submit_order(order_data=order_data)
            print(f"[ORDER SUCCESS] {side_str.upper()} {qty} {symbol} | "
                  f"Order ID: {order.id} | Status: {order.status}")
        except Exception as e:
            print(f"[ORDER FAILED] {side_str.upper()} {qty} {symbol} → {str(e)}")
            raise

    async def get_account(self):
        try:
            acc = self.trading.get_account()
            equity = getattr(acc, 'equity', 'MISSING')
            print(f"[ACCOUNT] Equity: ${equity} | Buying power: ${getattr(acc, 'buying_power', 'MISSING')}")
            return acc
        except Exception as e:
            print(f"[ACCOUNT FETCH FAILED] {str(e)}")
            raise
