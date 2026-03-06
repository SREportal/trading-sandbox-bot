#!/usr/bin/env bash
set -e

PYTHON_VERSION="3.11"

echo "🚀 Trading Sandbox Bot — startup"
echo "================================="

# ── 1. Check .env exists ──────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
  echo ""
  echo "⚠️  No .env file found."
  echo "   Run:  cp .env.example .env"
  echo "   Then fill in your Alpaca paper API keys."
  exit 1
fi

# ── 2. Ensure uv is available ─────────────────────────────────────────────────
if ! command -v uv &>/dev/null; then
  echo ""
  echo "❌ uv not found. Install it with:"
  echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
  echo "   Then restart your terminal and re-run ./start.sh"
  exit 1
fi

# ── 3. Create virtual environment if it doesn't exist ────────────────────────
if [ ! -d ".venv" ]; then
  echo "📦 Creating virtual environment (Python ${PYTHON_VERSION})..."
  uv venv --python "${PYTHON_VERSION}"
else
  echo "✅ Virtual environment already exists."
fi

# ── 4. Install / update dependencies ─────────────────────────────────────────
echo "📥 Installing dependencies..."
uv pip install -q -r requirements.txt

# ── 5. Launch the bot ─────────────────────────────────────────────────────────
echo ""
echo "▶️  Starting bot..."
echo ""
uv run python -u run_bot.py
