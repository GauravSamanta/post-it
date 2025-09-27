# Contributing to FastAPI React Boilerplate

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+
- Python 3.11+
- Git

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/fastapi-react-boilerplate.git
   cd fastapi-react-boilerplate
   ```

2. **Set up the development environment**
   ```bash
   docker-compose up -d
   ```

3. **Install pre-commit hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## 🔄 Development Workflow

### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Feature development branches
- `hotfix/*`: Critical bug fixes

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   pytest --cov=app

   # Frontend tests
   cd frontend
   npm test

   # Run linting
   npm run lint
   cd ../backend
   black --check .
   flake8 .
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

### Examples
```
feat: add user profile management
fix: resolve authentication token expiration
docs: update API documentation
style: format code with prettier
refactor: restructure user service
test: add unit tests for auth service
chore: update dependencies
```

## 🧪 Testing Guidelines

### Backend Testing
- Write unit tests for all new functions and classes
- Use pytest fixtures for test data
- Aim for >90% code coverage
- Test both success and error cases

```python
def test_create_user_success(client, test_user):
    response = client.post("/api/v1/users/", json=test_user)
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]

def test_create_user_duplicate_email(client, test_user):
    client.post("/api/v1/users/", json=test_user)
    response = client.post("/api/v1/users/", json=test_user)
    assert response.status_code == 400
```

### Frontend Testing
- Write unit tests for components and utilities
- Use React Testing Library for component tests
- Test user interactions and edge cases
- Mock external dependencies

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from '@/components/ui/button'

describe('Button', () => {
  it('handles click events', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    
    fireEvent.click(screen.getByRole('button'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

## 🎨 Code Style Guidelines

### Backend (Python)
- Use Black for code formatting (line length: 88)
- Use isort for import sorting
- Use type hints for all functions
- Follow PEP 8 naming conventions
- Write docstrings for public functions

```python
from typing import Optional
from sqlalchemy.orm import Session

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieve a user by email address.
    
    Args:
        db: Database session
        email: User's email address
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()
```

### Frontend (TypeScript/React)
- Use Prettier for code formatting
- Use meaningful component and variable names
- Prefer function components with hooks
- Use TypeScript interfaces for props
- Keep components small and focused

```typescript
interface UserProfileProps {
  user: User
  onUpdate: (user: User) => void
}

export function UserProfile({ user, onUpdate }: UserProfileProps) {
  const [isEditing, setIsEditing] = useState(false)
  
  return (
    <div className="user-profile">
      {/* Component content */}
    </div>
  )
}
```

## 📚 Documentation

### Code Documentation
- Write clear, concise comments
- Document complex algorithms or business logic
- Keep comments up-to-date with code changes

### API Documentation
- Use FastAPI's automatic documentation features
- Add descriptions to Pydantic models
- Include examples in docstrings

```python
class UserCreate(BaseModel):
    """Schema for creating a new user."""
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")
    full_name: Optional[str] = Field(None, description="User's full name")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword",
                "full_name": "John Doe"
            }
        }
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to reproduce**: Detailed steps to reproduce the bug
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**: OS, browser, versions, etc.
6. **Screenshots**: If applicable

### Bug Report Template
```markdown
## Bug Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
A clear description of what you expected to happen.

## Actual Behavior
A clear description of what actually happened.

## Environment
- OS: [e.g. Windows 10, macOS 12.0]
- Browser: [e.g. Chrome 96, Firefox 95]
- Node.js version: [e.g. 18.0.0]
- Python version: [e.g. 3.11.0]

## Additional Context
Add any other context about the problem here.
```

## 💡 Feature Requests

When requesting features, please include:

1. **Problem**: What problem does this solve?
2. **Solution**: Describe your proposed solution
3. **Alternatives**: Alternative solutions you've considered
4. **Use cases**: How would this feature be used?

## 🔍 Code Review Process

### For Contributors
- Ensure your code passes all tests and linting
- Write clear commit messages
- Keep pull requests focused and small
- Respond to feedback promptly

### For Reviewers
- Be constructive and respectful
- Focus on code quality, not personal preferences
- Suggest improvements with examples
- Approve when ready, request changes when needed

## 📋 Pull Request Checklist

Before submitting a pull request, ensure:

- [ ] Code follows the style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated if needed
- [ ] Commit messages follow conventional format
- [ ] No merge conflicts with target branch
- [ ] PR description clearly explains changes

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

## 📞 Getting Help

If you need help:
1. Check existing documentation
2. Search existing issues
3. Join our community discussions
4. Create a new issue with the "question" label

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to FastAPI React Boilerplate! 🚀

