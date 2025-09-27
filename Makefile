# FastAPI React Boilerplate Makefile

.PHONY: help install dev build test lint format clean docker-build docker-up docker-down

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies for both backend and frontend"
	@echo "  dev         - Start development servers"
	@echo "  build       - Build production assets"
	@echo "  test        - Run all tests"
	@echo "  lint        - Run linting for both backend and frontend"
	@echo "  format      - Format code for both backend and frontend"
	@echo "  clean       - Clean build artifacts and caches"
	@echo "  docker-build - Build Docker images"
	@echo "  docker-up   - Start Docker Compose services"
	@echo "  docker-down - Stop Docker Compose services"

# Installation
install: install-backend install-frontend

install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

# Development
dev: dev-backend dev-frontend

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

# Build
build: build-backend build-frontend

build-backend:
	cd backend && python -m build

build-frontend:
	cd frontend && npm run build

# Testing
test: test-backend test-frontend

test-backend:
	cd backend && pytest --cov=app --cov-report=term-missing

test-frontend:
	cd frontend && npm test

test-coverage:
	cd backend && pytest --cov=app --cov-report=html
	cd frontend && npm run test:coverage

# Linting
lint: lint-backend lint-frontend

lint-backend:
	cd backend && black --check .
	cd backend && isort --check-only .
	cd backend && flake8 .
	cd backend && mypy app

lint-frontend:
	cd frontend && npm run lint
	cd frontend && npm run format:check

# Formatting
format: format-backend format-frontend

format-backend:
	cd backend && black .
	cd backend && isort .

format-frontend:
	cd frontend && npm run format

# Database
db-init:
	cd backend && python scripts/init_db.py

db-migrate:
	cd backend && alembic upgrade head

db-revision:
	cd backend && alembic revision --autogenerate -m "$(message)"

db-reset:
	cd backend && rm -f app.db
	cd backend && alembic upgrade head
	cd backend && python scripts/init_db.py

# Cleaning
clean: clean-backend clean-frontend

clean-backend:
	cd backend && find . -type d -name "__pycache__" -exec rm -rf {} +
	cd backend && find . -type f -name "*.pyc" -delete
	cd backend && rm -rf .pytest_cache
	cd backend && rm -rf .coverage
	cd backend && rm -rf htmlcov
	cd backend && rm -rf dist
	cd backend && rm -rf build
	cd backend && rm -rf *.egg-info

clean-frontend:
	cd frontend && rm -rf node_modules
	cd frontend && rm -rf dist
	cd frontend && rm -rf coverage

# Docker
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-clean:
	docker-compose down -v
	docker system prune -f

# Production
prod-build:
	docker-compose -f docker-compose.prod.yml build

prod-up:
	docker-compose -f docker-compose.prod.yml up -d

prod-down:
	docker-compose -f docker-compose.prod.yml down

# Security
security-scan:
	cd backend && safety check
	cd frontend && npm audit --audit-level=high

# Documentation
docs-serve:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 &
	@echo "API documentation available at:"
	@echo "  Swagger UI: http://localhost:8000/docs"
	@echo "  ReDoc: http://localhost:8000/redoc"

# Setup for new developers
setup: install db-init
	@echo "Setup complete! Run 'make dev' to start development servers."

# CI/CD helpers
ci-install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm ci

ci-test: test lint

ci-build: build

# Health check
health:
	@curl -f http://localhost:8000/health || echo "Backend not running"
	@curl -f http://localhost:3000 || echo "Frontend not running"

