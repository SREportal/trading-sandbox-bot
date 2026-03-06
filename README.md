# Trading Sandbox Bot

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Paper Trading](https://img.shields.io/badge/Mode-Paper%20Trading-green)
![Brokers](https://img.shields.io/badge/Brokers-Alpaca%20%7C%20IBKR%20%7C%20Robinhood-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Educational](https://img.shields.io/badge/Purpose-Educational-blueviolet)

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

---

## How It Works

The bot runs a continuous async event loop. Every 60 seconds it:

1. Fetches recent OHLCV price bars from your broker
2. Runs each enabled strategy → computes technical indicators on a pandas DataFrame
3. If signal is `BUY` or `SELL` → sizes the position via the risk manager → places a market order
4. Sleeps 60 seconds and repeats

```
Every 60 seconds:
  for each strategy:
    for each symbol:
      bars = broker.get_bars(symbol)        ← OHLCV DataFrame
      signal = strategy.generate_signal(bars) ← BUY / SELL / HOLD
      if signal != HOLD:
        qty = risk_manager.calculate_quantity(equity, price)
        broker.place_order(symbol, signal, qty)
```

---

## Architecture

All components are wired through factory patterns — swap broker or strategy with a single config change, zero code edits.

```
┌──────────────────────────────────────────────────┐
│                   config.yaml                    │
│          (your only configuration file)          │
└──────────────────────┬───────────────────────────┘
                       │
               ┌───────▼────────┐
               │    main.py     │  ←  async event loop (60s cadence)
               └───┬────────┬───┘
                   │        │
        ┌──────────▼──┐  ┌──▼───────────┐
        │   Broker    │  │   Strategy   │
        │   Factory   │  │   Factory    │
        └──────┬──────┘  └──────┬───────┘
               │                │
   ┌───────────▼────┐  ┌────────▼──────────┐
   │ Alpaca         │  │ SMA Crossover     │
   │ IBKR           │  │ MACD Crossover    │
   │ Robinhood      │  │ Bollinger Breakout│
   └───────────┬────┘  └────────┬──────────┘
               │                │
               └───────┬────────┘
                       │
               ┌───────▼────────┐
               │  Risk Manager  │
               │ position sizing│
               └────────────────┘
```

**Design patterns used:**
- **Factory pattern** — brokers and strategies are interchangeable plugins
- **Abstract base classes** — `BrokerBase` and `StrategyBase` define the interface; each broker/strategy implements it
- **Async I/O** — all broker API calls use `asyncio` / `await` for non-blocking execution
- **YAML-driven config** — no hardcoded values; everything is runtime-configurable

---

## First Time Setup (Install Git + uv)

You only need two tools installed before running the bot. Follow the steps for your OS:

### Mac

Open **Terminal** (search "Terminal" in Spotlight) and run:

```bash
# 1. Install Git (part of Xcode Command Line Tools)
xcode-select --install

# 2. Install uv (Python + package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart Terminal after step 2, then continue to Quick Start.

---

### Windows

Open **PowerShell** (search "PowerShell" in Start menu) and run:

```powershell
# 1. Install Git
winget install --id Git.Git -e --source winget

# 2. Install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart PowerShell after step 2, then continue to Quick Start.

> If `winget` isn't available, download Git manually from https://git-scm.com/download/win

---

### Linux (Ubuntu / Debian)

Open a terminal and run:

```bash
# 1. Install Git
sudo apt update && sudo apt install -y git

# 2. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For Fedora/RHEL: replace `apt` with `dnf`. Restart terminal after step 2.

---

## Prerequisites

- Python 3.11+ (managed automatically by uv — no manual install needed)
- [uv](https://docs.astral.sh/uv/) — installed above
- Git — installed above
- Free Alpaca account (for easiest start)

---

## Quick Start (One Command)

```bash
git clone https://github.com/SREportal/trading-sandbox-bot.git
cd trading-sandbox-bot
cp .env.example .env   # fill in your Alpaca paper keys
./start.sh
```

Or with Make:

```bash
make setup   # create .venv + install deps
make run     # launch the bot
```

---

## Setup Alpaca Paper Account & Keys

1. Go to: https://app.alpaca.markets/signup (free, no credit card needed for paper trading)
2. Complete signup and **enable 2FA** (two-factor authentication) – **mandatory** for security
   → Profile → Security → Enable 2FA (use Google Authenticator or similar app)
3. After login → Profile (top right) → API Keys
4. Generate **Paper** keys:
   - **APCA-API-KEY-ID** (starts with `PK...`)
   - **APCA-API-SECRET-KEY** (long random string)
5. Copy both – you'll paste them into `.env` file next.

---

## Installation (Manual)

```bash
# Clone the repository
git clone https://github.com/SREportal/trading-sandbox-bot.git
cd trading-sandbox-bot

# Create virtual environment with Python 3.11
uv venv --python 3.11

# Install dependencies
uv pip install -r requirements.txt

# If you see NumPy-related errors, run:
uv pip install "numpy<2.0" --force-reinstall
uv pip install bottleneck --upgrade
```

---

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and paste your Alpaca paper keys:
   ```
   ALPACA_API_KEY=PKYOURFULL36CHARKEYHERE
   ALPACA_SECRET_KEY=yourlongsecretkeyhere
   ```
   No quotes, no extra spaces.

3. Edit `config.yaml` to choose broker, enable strategies, change symbols, etc.
   - Start with `mode: paper`
   - `broker.type: alpaca`
   - Enable 1–2 strategies to begin

---

## Running the Bot

```bash
uv run python run_bot.py
```

Expected output on startup:

```
🚀 Trading Sandbox Bot started in PAPER mode
Broker: ALPACA | Strategies: 2

🔄 Daily startup routine...
  → Cancelling all open orders...
[STARTUP] Cancelled 0 open order(s).
  → Closing all open positions...
[STARTUP] All positions closed.
  → Waiting 3s for orders to settle...
  → Running initial strategy scan...
Equity: $100000.00
✅ Startup complete.
```

**Every time the bot starts it will:**
1. Cancel all pending/unfilled orders
2. Close (sell) all open positions — starting each day flat
3. Immediately scan all strategies and open fresh positions based on current signals
4. Then continue scanning every 60 seconds

> **Note:** Outside US market hours, you may see few or no new bars (normal). Change interval to `"1Day"` in `config.yaml` for always-available historical data during testing.

---

## Common Issues & Fixes

- **"You must supply a method of authentication"**
  → Check `.env` file: keys correct? No spaces/quotes? Starts with `PK` for paper?

- **ModuleNotFoundError 'ib_insync'**
  → Change import in `brokers/ibkr.py` to `from ib_async import *` (we use the maintained fork)

- **TimeFrame has no attribute 'FiveMinute' / 'Minutes'**
  → Update `get_bars` in `alpaca.py` to use `TimeFrame(5, TimeFrameUnit.Minute)` syntax

- **NumPy / pyarrow / bottleneck errors** (`_ARRAY_API not found`)
  → Run `uv pip install "numpy<2.0" --force-reinstall` or recreate the venv: `rm -rf .venv && uv venv --python 3.11`

- **No bars fetched**
  → Normal outside trading hours. Use `"1Day"` interval for testing.

- **Other import / package errors**
  → Ensure your `.venv` exists (`uv venv --python 3.11`)
  → Reinstall: `uv pip install -r requirements.txt --force-reinstall`

---

## Next Steps

- Test thoroughly in paper mode
- Add Telegram/Discord alerts on signals
- Create custom strategies in `strategies/` folder
- Explore backtesting (future addition)
- Add a `--no-flatten` flag to skip position clearing on restart

---

Happy (paper) trading! 🚀
Always trade responsibly.
