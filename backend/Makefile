include .env
export $(shell sed 's/=.*//' .env)

.PHONY: help

help:
	@echo "Commands:"
	@echo "  install         : install dependencies"
	@echo "  run             : run the application"
	@echo "  format          : format the codebase using ruff"

install:
	uv sync

run:
	uvicorn app.main:app --reload --port $(PORT)

format:
	ruff check --select I --fix && ruff format
