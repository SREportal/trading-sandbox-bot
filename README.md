# Trading Sandbox Bot

**Configurable multi-broker, multi-strategy trading bot** – perfect for paper trading & learning.

**Features**
- One `config.yaml` to switch broker + strategies + parameters
- Market data always comes from the broker you trade with
- Built-in risk management
- Easy to add new strategies/brokers
- 100% sandbox-first

**Supported Brokers** (start with Alpaca – free & instant)
- Alpaca (recommended)
- Interactive Brokers
- Robinhood (crypto only – stocks unofficial)

**Strategies included**
- SMA Crossover + RSI filter
- MACD Crossover
- Bollinger Bands Breakout

## Quick Start
1. `mkdir trading-sandbox-bot && cd trading-sandbox-bot`
2. Create all files below
3. `pip install -r requirements.txt`
4. `cp .env.example .env` → fill your keys
5. Edit `config.yaml` (set broker & enable strategies)
6. `python run_bot.py`

Always start with `mode: paper`.

Happy sandbox trading! 🚀
