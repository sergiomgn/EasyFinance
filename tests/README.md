# EasyFinance Test Suite

This directory contains comprehensive unit tests for the EasyFinance application.

## Structure

```
tests/
├── __init__.py                          # Test package initialization
├── conftest.py                          # Pytest configuration and fixtures
├── requirements-test.txt                # Test dependencies
├── test_main.py                         # Main test module with documentation
├── test_utils.py                        # Test utilities and helpers
├── test_models_financial.py             # Tests for financial models
├── test_models_user.py                  # Tests for user models
├── test_models_security.py              # Tests for security models
├── test_auth_oauth2.py                  # Tests for OAuth2 authentication
├── test_controller_databaseI.py         # Tests for database interface
├── test_controller_sql.py               # Tests for SQL implementation
├── test_middleware_auto_refresh.py      # Tests for auto-refresh middleware
└── test_api.py                          # Tests for API endpoints
```

## Installation

1. Install test dependencies:
```bash
pip install -r tests/requirements-test.txt
```

2. Install the main application dependencies:
```bash
pip install -r src/requirements.txt
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_models_user.py
```

### Run tests with coverage
```bash
pytest --cov=src --cov-report=html
```

### Run tests by marker
```bash
pytest -m unit          # Run only unit tests
pytest -m integration   # Run only integration tests
pytest -m auth          # Run only authentication tests
```

### Run tests with verbose output
```bash
pytest -v
```

## Test Categories

### Unit Tests
- **Models**: Test Pydantic models for validation and data integrity
- **Authentication**: Test JWT token creation, validation, and refresh
- **Database Interface**: Test abstract database interface
- **SQL Implementation**: Test SQLite database operations
- **Middleware**: Test middleware components

### Integration Tests
- **API Endpoints**: Test FastAPI endpoints with mocked dependencies
- **Database Operations**: Test complete database workflows
- **Authentication Flow**: Test end-to-end authentication

## Test Utilities

The `test_utils.py` module provides helpful utilities:

- **TestDataFactory**: Create test data objects easily
- **DatabaseTestHelper**: Set up and manage test databases
- **TokenTestHelper**: Create and validate JWT tokens for testing
- **ValidationHelper**: Common assertion helpers
- **TempDatabaseContext**: Context manager for temporary databases

### Example Usage

```python
from tests.test_utils import TestDataFactory, TempDatabaseContext

# Create test data
user = TestDataFactory.create_user("testuser", "password123")
expense = TestDataFactory.create_expense(amount=50.0, category="Groceries")

# Use temporary database
with TempDatabaseContext() as db:
    await db.create_user(user)
    exists, error = await db.user_exists(user)
    assert exists is True
```

## Test Configuration

The `pytest.ini` file configures:
- Test discovery patterns
- Coverage settings (minimum 80% coverage)
- Async test mode
- Test markers for categorization
- Output formatting

## Environment Setup

Tests automatically configure:
- Test environment variables (`JWT_SECRET_KEY`)
- Temporary databases for isolation
- Mock objects for external dependencies

## Continuous Integration

Tests are designed to run in CI/CD environments with:
- No external dependencies
- Isolated test databases
- Deterministic behavior
- Comprehensive coverage reporting

## Best Practices

1. **Isolation**: Each test is independent and can run in any order
2. **Mocking**: External dependencies are mocked to ensure fast, reliable tests
3. **Coverage**: Aim for high test coverage while focusing on meaningful tests
4. **Documentation**: Tests serve as documentation for expected behavior
5. **Performance**: Tests run quickly to support rapid development

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `src` directory is in Python path (handled by `conftest.py`)
2. **Database Locks**: Tests use temporary databases to avoid conflicts
3. **Async Issues**: Use `pytest-asyncio` for async function testing
4. **Missing Dependencies**: Install all requirements from `requirements-test.txt`

### Debug Mode
```bash
pytest -v -s                    # Verbose with print statements
pytest --tb=long                # Full tracebacks
pytest --pdb                    # Drop into debugger on failure
```

## Contributing

When adding new tests:

1. Follow the naming convention: `test_<module>_<class>.py`
2. Use appropriate test markers (`@pytest.mark.unit`, etc.)
3. Include docstrings explaining test purpose
4. Use test utilities for common operations
5. Ensure tests are isolated and repeatable
6. Add new test dependencies to `requirements-test.txt`

## Coverage Goals

- **Models**: 100% coverage (simple validation logic)
- **Controllers**: 90%+ coverage (core business logic)
- **Authentication**: 95%+ coverage (security critical)
- **API Endpoints**: 85%+ coverage (integration focused)
- **Overall**: 80%+ minimum coverage

## Performance

The test suite is designed to run quickly:
- Unit tests: < 1 second each
- Integration tests: < 5 seconds each
- Full suite: < 30 seconds

For slower tests, use the `@pytest.mark.slow` marker.
