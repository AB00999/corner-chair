# Contributing to Corner Chair

Thank you for your interest in contributing to the Corner Chair barbershop booking system!

## 📋 Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- pip/venv

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/AB00999/corner-chair.git
cd corner-chair

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r barber-booking-demo/requirements.txt

# Run tests
python -m pytest barber-booking-demo/tests/

# Run app
python barber-booking-demo/app.py
```

Visit `http://localhost:5001`

## 🔧 Making Changes

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Keep changes focused and atomic
- Follow PEP 8 style guide
- Add tests for new functionality
- Update documentation

### 3. Test Your Changes
```bash
python -m pytest barber-booking-demo/tests/ -v
python -m pytest barber-booking-demo/tests/ --cov=barber_booking_demo
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add new feature description"
```

Use conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Tests
- `refactor:` - Code refactoring
- `style:` - Style changes (formatting, etc.)
- `perf:` - Performance improvements

### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Create a Pull Request with:
- Clear title describing the change
- Detailed description of what changed and why
- Reference any related issues
- Screenshots for UI changes

## 📝 Writing Tests

Place tests in `barber-booking-demo/tests/` directory.

```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_booking_page_loads(client):
    response = client.get('/book')
    assert response.status_code == 200
```

## 📚 Documentation

- Update README.md for user-facing changes
- Add docstrings to Python functions
- Update CONTRIBUTING.md if adding new processes
- Include examples where helpful

### Docstring Format
```python
def schedule_appointment(date, time, service):
    """
    Schedule a new appointment.
    
    Args:
        date (str): Appointment date (YYYY-MM-DD)
        time (str): Appointment time (HH:MM)
        service (str): Service type
    
    Returns:
        dict: Appointment confirmation details
    
    Raises:
        ValueError: If date/time is invalid or in the past
        DatabaseError: If unable to save to database
    """
```

## 🐛 Reporting Issues

Create an issue with:
- Clear, descriptive title
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots/logs if applicable
- Your environment details

## 💡 Feature Requests

Describe the feature with:
- Use case and motivation
- Proposed behavior
- Possible implementation approach
- Any alternatives considered

## 🎨 Code Style

### Python
```python
# Follow PEP 8
# Use meaningful variable names
# Keep functions focused and small
# Add type hints where possible

def validate_email(email: str) -> bool:
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

### HTML/CSS
```html
<!-- Use semantic HTML -->
<!-- Indent with 2 spaces -->
<!-- Use meaningful class names -->
<div class="booking-form">
  <h1 class="booking-form__title">Book an Appointment</h1>
</div>
```

## 🚀 Pull Request Process

1. **Before submitting:**
   - Tests pass locally
   - No linting errors
   - Documentation updated
   - Commits are clean and well-formatted

2. **After submitting:**
   - CI/CD checks must pass
   - At least one review required
   - Address reviewer feedback
   - Merge when approved

3. **After merge:**
   - Delete your feature branch
   - Close any related issues
   - Update release notes if needed

## 📦 Release Process

Maintainers follow semantic versioning:
- `MAJOR.MINOR.PATCH` (e.g., 1.2.3)
- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes

## 🤝 Community

- Be respectful and constructive
- Help review other PRs
- Participate in discussions
- Share your ideas and improvements

## 📞 Questions?

- Check existing issues/discussions
- Ask in pull request comments
- Create a discussion thread

## 📄 License

By contributing, you agree that your contributions will be licensed under the same MIT License as the project.

---

**Thank you for helping make Corner Chair better!** 🎉

