.PHONY: setup run clean help

ENV_NAME  = trading-clean
PYTHON    = 3.11

help:
	@echo ""
	@echo "  Trading Sandbox Bot"
	@echo "  ───────────────────"
	@echo "  make setup   Create conda env and install dependencies"
	@echo "  make run     Launch the bot"
	@echo "  make clean   Remove the conda env"
	@echo ""

setup:
	@echo "📦 Creating conda env '$(ENV_NAME)' with Python $(PYTHON)..."
	@conda create -y -n $(ENV_NAME) python=$(PYTHON) 2>/dev/null || true
	@echo "📥 Installing dependencies..."
	@conda run -n $(ENV_NAME) pip install -q -r requirements.txt
	@echo "✅ Setup complete. Run 'make run' to start the bot."

run:
	@if [ ! -f ".env" ]; then \
		echo "⚠️  No .env file found. Run: cp .env.example .env"; \
		exit 1; \
	fi
	@echo "▶️  Starting Trading Sandbox Bot..."
	@conda run -n $(ENV_NAME) python run_bot.py

clean:
	@echo "🗑  Removing conda env '$(ENV_NAME)'..."
	@conda env remove -y -n $(ENV_NAME)
	@echo "✅ Done."
