# =========================
# Makefile for FastAPI + asyncpg
# =========================

# Variables
APP_MODULE=app.main:app
HOST=0.0.0.0
PORT=8000
SRC_DIRS=app tests

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install     - Install dependencies via uv"
	@echo "  make run         - Run FastAPI server with hot reload"
	@echo "  make migrate     - Apply database migrations"
	@echo "  make test        - Run tests with pytest"
	@echo "  make lint        - Lint code with ruff"
	@echo "  make format      - Autoformat code with black"

# Install dependencies
.PHONY: install
install:
	uv install

# Run FastAPI server
.PHONY: run
run:
	uv run uvicorn $(APP_MODULE) --reload --host $(HOST) --port $(PORT)

# Apply database migrations
.PHONY: migrate
migrate:
	uv run -m scripts.migrate

# Run tests
.PHONY: test
test:
	uv run pytest $(SRC_DIRS) --maxfail=1 --disable-warnings -q

# Lint code
.PHONY: lint
lint:
	uv run ruff check $(SRC_DIRS)

# Autoformat code
.PHONY: format
format:
	uv run black $(SRC_DIRS)
