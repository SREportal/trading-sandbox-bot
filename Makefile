.PHONY: setup run clean help

PYTHON = 3.11

help:
	@echo ""
	@echo "  Trading Sandbox Bot"
	@echo "  ───────────────────"
	@echo "  make setup   Create virtual env and install dependencies"
	@echo "  make run     Launch the bot"
	@echo "  make clean   Remove the virtual env"
	@echo ""

setup:
	@echo "📦 Creating virtual environment (Python $(PYTHON))..."
	@uv venv --python $(PYTHON)
	@echo "📥 Installing dependencies..."
	@uv pip install -q -r requirements.txt
	@echo "✅ Setup complete. Run 'make run' to start the bot."

run:
	@if [ ! -f ".env" ]; then \
		echo "⚠️  No .env file found. Run: cp .env.example .env"; \
		exit 1; \
	fi
	@echo "▶️  Starting Trading Sandbox Bot..."
	@uv run python run_bot.py

clean:
	@echo "🗑  Removing virtual environment..."
	@rm -rf .venv
	@echo "✅ Done."
