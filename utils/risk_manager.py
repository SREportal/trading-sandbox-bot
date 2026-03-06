class RiskManager:
    def __init__(self, config):
        self.max_pct = config.get("max_position_size_pct", 5.0)

    def can_place_trade(self, account, symbol, signal):
        try:
            buying_power = float(getattr(account, 'buying_power', 0) or 0)
            equity = float(getattr(account, 'equity', 100000) or 100000)
            required = equity * (self.max_pct / 100)
            if buying_power < required:
                print(f"[SKIP] {symbol} — insufficient buying power (${buying_power:.2f} < ${required:.2f} needed)")
                return False
        except (ValueError, TypeError):
            pass
        return True

    def calculate_quantity(self, account, price: float):
        equity_str = getattr(account, 'equity', None)

        if equity_str is None:
            print("Warning: Equity is None from Alpaca → using default $100,000 paper balance")
            equity = 100000.0
        else:
            try:
                equity = float(equity_str)
                if equity <= 0:
                    print("Warning: Equity is zero or negative → using default $100,000")
                    equity = 100000.0
            except (ValueError, TypeError):
                print("Warning: Invalid equity value → using default $100,000")
                equity = 100000.0

        max_dollars = equity * (self.max_pct / 100)
        qty = max(1, int(max_dollars / price))
        print(f"Calculated qty: {qty} at price {price} (equity used: {equity})")  # debug
        return qty
