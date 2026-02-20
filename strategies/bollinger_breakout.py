import pandas_ta_classic as ta
from .base import StrategyBase

class BollingerBreakout(StrategyBase):
    def generate_signal(self, df, params):
        bb = ta.bbands(df["close"], length=params.get("period", 20), std=params.get("std", 2.0))
        df = pd.concat([df, bb], axis=1)
        latest = df.iloc[-1]
        if latest["close"] > latest["BBU_20_2.0"]:
            return "BUY"
        elif latest["close"] < latest["BBL_20_2.0"]:
            return "SELL"
        return "HOLD"
