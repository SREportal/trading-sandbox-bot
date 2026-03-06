# Changelog

All notable changes to this project will be documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

---

## [1.1.0] - 2026-03-05

### Added
- **Architecture diagram** in README showing factory pattern and async event loop
- **How It Works** section in README with event loop pseudocode
- **First Time Setup** section in README with install instructions for Mac, Windows, and Linux
- **GitHub badges** (Python version, paper trading mode, brokers, license, educational purpose)
- **Buying power guard** in `RiskManager.can_place_trade()` — skips orders gracefully when account has insufficient buying power instead of spamming failed API calls

### Fixed
- `strategies/macd_crossover.py` — missing `import pandas as pd` caused `NameError: name 'pd' is not defined` on every MACD symbol scan

### Changed
- Replaced **conda** with **uv** across `start.sh`, `Makefile`, and README
  - `start.sh` now creates `.venv` via `uv venv` and runs with `uv run`
  - `Makefile` targets updated: `make setup` and `make run` use uv
  - `make clean` now removes `.venv` instead of a conda environment
- README Prerequisites updated: conda removed, uv added with install command
- README Installation (Manual) section updated to use `uv venv` + `uv pip install`
- README Running the Bot updated to `uv run python run_bot.py`
- README Common Issues updated: all pip/conda references replaced with uv equivalents

---

## [1.0.0] - 2026-03-01

### Added
- Initial release of trading-sandbox-bot
- Alpaca broker integration (paper + live)
- Interactive Brokers (IBKR) integration via `ib_async`
- Robinhood integration (crypto/demo only)
- SMA Crossover strategy with RSI filter
- MACD Crossover strategy
- Bollinger Bands Breakout strategy
- Factory pattern for brokers and strategies
- `RiskManager` for equity-based position sizing
- Daily startup routine: cancel orders, close positions, re-scan
- `config.yaml` single-file configuration
- `.env` support for API credentials
- `start.sh` one-command launch script
- `Makefile` with `setup`, `run`, `clean` targets
