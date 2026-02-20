class RiskManager:
    def __init__(self, config):
        self.max_pct = config.get("max_position_size_pct", 5.0)

    def can_place_trade(self, account, symbol, signal):
        return True  # add more rules later

    def calculate_quantity(self, account, price):
        equity = float(getattr(account, "equity", 10000))
        max_dollars = equity * self.max_pct / 100
        return max(1, int(max_dollars / price))
