import yaml
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)
import os
import asyncio
import time

from brokers.factory import BrokerFactory
from strategies.factory import StrategyFactory
from utils.risk_manager import RiskManager

load_dotenv()

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


async def run_strategies(broker, strategies, risk_manager):
    """Fetch bars, generate signals, and place orders for all strategies."""
    account = await broker.get_account()
    print(f"Equity: ${float(account.equity):.2f}" if hasattr(account, "equity") else "Connected")

    for strat in strategies:
        for symbol in strat.symbols:
            try:
                df = await broker.get_bars(symbol, strat.interval, limit=500)
                if len(df) < 100:
                    continue
                signal = strat.generate_signal(df, strat.params)
                if signal in ["BUY", "SELL"]:
                    print(f"[{strat.name.upper()}] {symbol} → {signal}")
                    if risk_manager.can_place_trade(account, symbol, signal):
                        qty = risk_manager.calculate_quantity(account, df.iloc[-1]["close"])
                        await broker.place_order(symbol, signal, qty)
            except Exception as e:
                print(f"[{strat.name.upper()}] {symbol} error: {e}")


async def startup_routine(broker, strategies, risk_manager):
    """Run once at bot start: flatten all positions, then immediately scan for signals."""
    print("\n🔄 Daily startup routine...")

    print("  → Cancelling all open orders...")
    await broker.cancel_all_orders()

    print("  → Closing all open positions...")
    await broker.close_all_positions()

    print("  → Waiting 3s for orders to settle...")
    await asyncio.sleep(3)

    print("  → Running initial strategy scan...")
    await run_strategies(broker, strategies, risk_manager)

    print("✅ Startup complete.\n")


async def main():
    broker = BrokerFactory.create(config)
    strategies = StrategyFactory.create_enabled_strategies(config["strategies"])
    risk_manager = RiskManager(config.get("risk_management", {}))

    print(f"🚀 Trading Sandbox Bot started in **{config['mode'].upper()}** mode")
    print(f"Broker: {config['broker']['type'].upper()} | Strategies: {len(strategies)}")

    await startup_routine(broker, strategies, risk_manager)

    while True:
        try:
            await run_strategies(broker, strategies, risk_manager)
        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(60)  # check every minute

if __name__ == "__main__":
    asyncio.run(main())
