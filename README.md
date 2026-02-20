# Trading Sandbox Bot

A simple, configurable Python trading bot for paper and live trading.  
You only need to edit **one file** (`config.yaml`) to change broker, strategies, symbols, intervals, and parameters.

**Supported Brokers**  
- **Alpaca** (recommended for beginners – free paper trading)  
- Interactive Brokers (professional, requires TWS/IB Gateway running locally)  
- Robinhood (unofficial – crypto only recommended; stock trading risks account restrictions)

**Included Strategies** (simple explanations for non-finance users)

- **SMA Crossover with RSI filter**  
  Looks at two moving averages (short-term and long-term).  
  - Buys when the short one crosses **above** the long one (trend may be going up)  
  - Sells when the short one crosses **below** the long one (trend may be going down)  
  - RSI filter prevents buying when the stock is already very expensive (overbought) or selling when it's very cheap (oversold)

- **MACD Crossover**  
  A momentum indicator that shows the relationship between two moving averages.  
  - Buys when the MACD line crosses **above** the signal line (momentum turning positive)  
  - Sells when it crosses **below** (momentum turning negative)

- **Bollinger Bands Breakout**  
  Plots a moving average with upper and lower bands (based on volatility).  
  - Buys when price breaks **above** the upper band (strong upward move)  
  - Sells when price breaks **below** the lower band (strong downward move)

**Important Disclaimer**  
This is for **educational purposes only**. Trading involves substantial risk of loss.  
Always start and stay in **paper mode** (simulated money).  
Never use real money until you fully understand the risks. This is **not** financial advice.

## Prerequisites

- Python 3.11+ (conda recommended)
- Git
- Free Alpaca account (for easiest start)

## Setup Alpaca Paper Account & Keys

1. Go to: https://app.alpaca.markets/signup (free, no credit card needed for paper trading)
2. Complete signup and **enable 2FA** (two-factor authentication) – **mandatory** for security  
   → Profile → Security → Enable 2FA (use Google Authenticator or similar app)
3. After login → Profile (top right) → API Keys
4. Generate **Paper** keys:
   - **APCA-API-KEY-ID** (starts with `PK...`)
   - **APCA-API-SECRET-KEY** (long random string)
5. Copy both – you’ll paste them into `.env` file next.

## Installation

```bash
# Clone the repository
git clone https://github.com/SREportal/trading-sandbox-bot.git
cd trading-sandbox-bot

# Create clean conda environment (avoids version conflicts)
conda create -n trading-clean python=3.11
conda activate trading-clean

# Install dependencies
pip install -r requirements.txt

# If you see NumPy-related errors, run:
pip install "numpy<2.0" --force-reinstall
pip install bottleneck --upgrade

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env

2. Open `.env` and paste your Alpaca paper keys:
ALPACA_API_KEY=PKYOURFULL36CHARKEYHERE
ALPACA_SECRET_KEY=yourlongsecretkeyhere
text- No quotes, no extra spaces.

3. Edit `config.yaml` to choose broker, enable strategies, change symbols, etc.
- Start with `mode: paper`
- `broker.type: alpaca`
- Enable 1–2 strategies to begin

Expected first output:
text🚀 Trading Sandbox Bot started in PAPER mode
Broker: ALPACA | Strategies: 2
Equity: $100000.00
The bot will then:

Fetch recent price data (bars)
Run selected strategies every ~60 seconds
Print BUY / SELL / HOLD signals when conditions are met

Note: Outside US market hours, you may see few or no new bars (normal). Change interval to "1Day" in config.yaml for always-available historical data during testing.

## Running the Bot

```bash
conda activate trading-clean
python run_bot.py

## Common Issues & Fixes

- **"You must supply a method of authentication"**  
  → Check `.env` file: keys correct? No spaces/quotes? Starts with `PK` for paper?

- **ModuleNotFoundError 'ib_insync'**  
  → Change import in `brokers/ibkr.py` to `from ib_async import *` (we use the maintained fork)

- **TimeFrame has no attribute 'FiveMinute' / 'Minutes'**  
  → Update `get_bars` in `alpaca.py` to use `TimeFrame(5, TimeFrameUnit.Minute)` syntax

- **NumPy / pyarrow / bottleneck errors** (`_ARRAY_API not found`)  
  → Run `pip install "numpy<2.0" --force-reinstall` or use fresh conda env

- **No bars fetched**  
  → Normal outside trading hours. Use `"1Day"` interval for testing.

- **Other import / package errors**  
  → Ensure you're in the correct conda env (`conda activate trading-clean`)  
  → Reinstall: `pip install -r requirements.txt --force-reinstall`

## Next Steps

- Test thoroughly in paper mode  
- Add Telegram/Discord alerts on signals  
- Create custom strategies in `strategies/` folder  
- Explore backtesting (future addition)

Happy (paper) trading! 🚀  
Always trade responsibly.
