# Post-It Notes API

A production-ready FastAPI application for managing post-it notes.

## Features

- Production-Ready: Structured logging, security headers, error handling
- Authentication: JWT-based auth with access/refresh tokens
- Database: SQLAlchemy with connection pooling
- Validation: Comprehensive request/response validation
- Monitoring: Health checks with database connectivity
- Security: CORS, trusted hosts, password hashing
- Middleware: Request logging, compression, security headers
- Environment-aware: Development/staging/production configs

## Quick Start

1. **Setup Environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # Windows:
   .venv\Scripts\activate
   # Unix/MacOS:
   source .venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   # Copy example environment file
   cp env.example .env
   
   # Edit .env file with your settings
   # Make sure SECRET_KEY is at least 32 characters
   ```

3. **Initialize Database**
   ```bash
   python scripts/init_db.py
   ```

4. **Run Application**
   ```bash
   # Development
   python run.py
   
   # Or using uvicorn directly
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Documentation

When running in development mode:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Health Checks

- Basic: `GET /health`
- Detailed: `GET /health/detailed` (includes database check)

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Runtime environment (development/staging/production) | development |
| `DEBUG` | Enable debug mode | false |
| `SECRET_KEY` | JWT secret key (min 32 chars) | auto-generated |
| `DATABASE_URL` | Database connection string | sqlite:///./app.db |
| `LOG_LEVEL` | Logging level | INFO |

## Production Deployment

For production deployment:

1. Set `ENVIRONMENT=production` in your `.env`
2. Use a proper database (PostgreSQL recommended)
3. Set a secure `SECRET_KEY`
4. Configure proper CORS origins
5. Use a reverse proxy (nginx) with SSL

```bash
# Production run with multiple workers
python run.py  # Automatically configures for production
```

## Security Features

- JWT authentication with refresh tokens
- Password hashing with bcrypt
- Security headers (HSTS, CSP, etc.)
- Request/response logging with request IDs
- Rate limiting ready (via middleware)
- Environment-based documentation hiding

## Development

```bash
# Run with auto-reload
python run.py

# Initialize/reset database
python scripts/init_db.py

# Run tests
pytest

# Code formatting
black .
isort .

# Linting
flake8
mypy .
```

## Project Structure

```
backend/
├── app/
│   ├── api/v1/          # API routes
│   ├── core/            # Core functionality
│   │   ├── config.py    # Settings management
│   │   ├── database.py  # Database setup
│   │   ├── logging.py   # Structured logging
│   │   ├── middleware.py # Custom middleware
│   │   └── security.py  # Auth & security
│   ├── crud/            # Database operations
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   └── main.py          # Application factory
├── scripts/             # Utility scripts
├── tests/              # Test suite
└── run.py              # Production runner
```
