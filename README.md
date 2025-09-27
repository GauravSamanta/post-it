# FastAPI + React Boilerplate

A production-ready, scalable boilerplate template built with FastAPI and React, following industry best practices and modern development standards.

## 🚀 Features

### Backend (FastAPI)
- **FastAPI Framework**: High-performance Python API with automatic documentation
- **Authentication**: JWT-based authentication with refresh tokens
- **Database**: SQLAlchemy ORM with Alembic migrations
- **Security**: Password hashing, CORS, trusted hosts, input validation
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **Testing**: Comprehensive test suite with pytest
- **Code Quality**: Black, isort, flake8, mypy for code formatting and linting

### Frontend (React)
- **React 18**: Latest React with TypeScript for type safety
- **Modern Tooling**: Vite for fast development and building
- **UI Components**: Radix UI primitives with Tailwind CSS styling
- **State Management**: Zustand for lightweight state management
- **Data Fetching**: TanStack Query (React Query) for server state
- **Form Handling**: React Hook Form with Zod validation
- **Testing**: Vitest and Testing Library for component testing
- **Code Quality**: ESLint, Prettier for code formatting and linting

### DevOps & Infrastructure
- **Containerization**: Docker and Docker Compose for development and production
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Security Scanning**: Trivy and dependency checks
- **Database**: PostgreSQL with Redis for caching
- **Reverse Proxy**: Nginx configuration for production

## 📁 Project Structure

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality (config, security, database)
│   │   ├── crud/           # Database operations
│   │   ├── models/         # SQLAlchemy models
│   │   └── schemas/        # Pydantic schemas
│   ├── tests/              # Backend tests
│   ├── alembic/            # Database migrations
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pyproject.toml
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── stores/         # Zustand stores
│   │   ├── lib/            # Utilities and API client
│   │   └── test/           # Frontend tests
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.ts
├── .github/workflows/      # CI/CD pipelines
├── docker-compose.yml      # Development environment
└── nginx.conf             # Nginx configuration
```

## 🛠️ Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Development with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fastapi-react-boilerplate
   ```

2. **Start the development environment**
   ```bash
   docker-compose up -d
   ```

3. **Access the applications**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

### Local Development

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest --cov=app
```

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:coverage
```

### Run All Tests
```bash
# With Docker Compose
docker-compose exec backend pytest
docker-compose exec frontend npm test
```

## 🚀 Deployment

### Production Build

1. **Build Docker images**
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Deploy with Docker Compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Environment Variables

#### Backend (.env)
```env
# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=480
REFRESH_TOKEN_EXPIRE_MINUTES=43200

# Database
DATABASE_URL=postgresql://user:password@localhost/dbname

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Superuser
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=changethis
```

#### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000
```

## 📚 API Documentation

The API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Authentication

The API uses JWT tokens for authentication:

1. **Login**: POST `/api/v1/auth/login`
2. **Get current user**: GET `/api/v1/auth/me`
3. **Refresh token**: POST `/api/v1/auth/refresh`

### User Management

- **Create user**: POST `/api/v1/users/`
- **Get users**: GET `/api/v1/users/`
- **Get user by ID**: GET `/api/v1/users/{user_id}`
- **Update user**: PUT `/api/v1/users/{user_id}`

## 🔧 Development Guidelines

### Code Style

#### Backend
- Use Black for code formatting
- Use isort for import sorting
- Use flake8 for linting
- Use mypy for type checking

```bash
black .
isort .
flake8 .
mypy app
```

#### Frontend
- Use Prettier for code formatting
- Use ESLint for linting
- Use TypeScript for type safety

```bash
npm run format
npm run lint
npm run lint:fix
```

### Git Workflow

1. Create feature branch from `develop`
2. Make changes and commit with conventional commits
3. Push branch and create pull request
4. CI/CD pipeline runs tests and checks
5. Merge to `develop` after review
6. Deploy to production from `main`

### Conventional Commits

```
feat: add new user registration endpoint
fix: resolve authentication token expiration issue
docs: update API documentation
style: format code with prettier
refactor: restructure user service
test: add unit tests for auth service
chore: update dependencies
```

## 🔒 Security

### Security Features
- JWT authentication with refresh tokens
- Password hashing with bcrypt
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- XSS protection with content security policy
- Rate limiting (configurable)

### Security Best Practices
- Use environment variables for secrets
- Regular dependency updates
- Security scanning in CI/CD
- HTTPS in production
- Database connection encryption
- Secure headers configuration

## 📊 Monitoring & Logging

### Logging
- Structured logging with structlog
- Request/response logging
- Error tracking
- Performance monitoring

### Health Checks
- Backend: `/health` endpoint
- Database connectivity check
- Redis connectivity check
- Docker health checks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Development Setup for Contributors

1. **Install pre-commit hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. **Run quality checks**
   ```bash
   # Backend
   cd backend
   black --check .
   isort --check-only .
   flake8 .
   mypy app
   pytest

   # Frontend
   cd frontend
   npm run lint
   npm run format:check
   npm test
   ```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [React](https://reactjs.org/) - A JavaScript library for building user interfaces
- [Tailwind CSS](https://tailwindcss.com/) - A utility-first CSS framework
- [Radix UI](https://www.radix-ui.com/) - Low-level UI primitives
- [TanStack Query](https://tanstack.com/query) - Powerful data synchronization for React

## 📞 Support

If you have any questions or need help, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

---

**Happy coding! 🚀**
