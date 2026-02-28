#!/usr/bin/env bash
set -e

ENV_NAME="trading-clean"
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

# ── 2. Ensure conda is available ─────────────────────────────────────────────
if ! command -v conda &>/dev/null; then
  echo ""
  echo "❌ conda not found. Please install Miniconda or Anaconda first:"
  echo "   https://docs.conda.io/en/latest/miniconda.html"
  exit 1
fi

# ── 3. Create conda env if it doesn't exist ──────────────────────────────────
if conda env list | grep -q "^${ENV_NAME} "; then
  echo "✅ Conda env '${ENV_NAME}' already exists."
else
  echo "📦 Creating conda env '${ENV_NAME}' (Python ${PYTHON_VERSION})..."
  conda create -y -n "${ENV_NAME}" python="${PYTHON_VERSION}"
fi

# ── 4. Install / update dependencies ─────────────────────────────────────────
echo "📥 Installing dependencies..."
conda run -n "${ENV_NAME}" pip install -q -r requirements.txt

# ── 5. Launch the bot ─────────────────────────────────────────────────────────
echo ""
echo "▶️  Starting bot..."
echo ""
conda run -n "${ENV_NAME}" python run_bot.py
