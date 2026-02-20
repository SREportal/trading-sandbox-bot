import pandas_ta_classic as ta
from .base import StrategyBase

class SMACrossover(StrategyBase):
    def generate_signal(self, df, params):
        fast = params.get("fast", 50)
        slow = params.get("slow", 200)
        df["sma_fast"] = ta.sma(df["close"], length=fast)
        df["sma_slow"] = ta.sma(df["close"], length=slow)
        df["rsi"] = ta.rsi(df["close"], length=params.get("rsi_period", 14))

        latest = df.iloc[-1]
        if latest["sma_fast"] > latest["sma_slow"] and latest["rsi"] < params.get("rsi_buy_threshold", 70):
            return "BUY"
        elif latest["sma_fast"] < latest["sma_slow"] and latest["rsi"] > params.get("rsi_sell_threshold", 30):
            return "SELL"
        return "HOLD"
