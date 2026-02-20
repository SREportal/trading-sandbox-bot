from .alpaca import AlpacaBroker
from .ibkr import IBKRBroker
from .robinhood import RobinhoodBroker

class BrokerFactory:
    @staticmethod
    def create(config):
        t = config["broker"]["type"].lower()
        if t == "alpaca":
            return AlpacaBroker(config)
        elif t == "ibkr":
            return IBKRBroker(config)
        elif t == "robinhood":
            return RobinhoodBroker(config)
        raise ValueError(f"Unknown broker type: {t}")
