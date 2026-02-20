from .sma_crossover import SMACrossover
from .macd_crossover import MACDCrossover
from .bollinger_breakout import BollingerBreakout

class StrategyFactory:
    @staticmethod
    def create_enabled_strategies(configs):
        strategies = []
        for cfg in configs:
            if cfg.get("enabled"):
                name = cfg["name"]
                if name == "sma_crossover":
                    strategies.append(SMACrossover(cfg))
                elif name == "macd_crossover":
                    strategies.append(MACDCrossover(cfg))
                elif name == "bollinger_breakout":
                    strategies.append(BollingerBreakout(cfg))
        return strategies
