import pandas_ta as ta
from .base import StrategyBase

class MACDCrossover(StrategyBase):
    def generate_signal(self, df, params):
        macd = ta.macd(df["close"])
        df = pd.concat([df, macd], axis=1)
        latest = df.iloc[-1]
        if latest["MACD_12_26_9"] > latest["MACDs_12_26_9"] and latest["MACDh_12_26_9"] > 0:
            return "BUY"
        elif latest["MACD_12_26_9"] < latest["MACDs_12_26_9"] and latest["MACDh_12_26_9"] < 0:
            return "SELL"
        return "HOLD"
