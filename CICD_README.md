# EasyFinance CI/CD Pipeline

[![CI/CD Pipeline](https://github.com/yourusername/easyfinance/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/yourusername/easyfinance/actions/workflows/ci-cd.yml)
[![CodeQL](https://github.com/yourusername/easyfinance/actions/workflows/codeql.yml/badge.svg)](https://github.com/yourusername/easyfinance/actions/workflows/codeql.yml)
[![Pre-commit](https://github.com/yourusername/easyfinance/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/yourusername/easyfinance/actions/workflows/pre-commit.yml)
[![codecov](https://codecov.io/gh/yourusername/easyfinance/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/easyfinance)

A comprehensive CI/CD pipeline for the EasyFinance personal finance management application built with FastAPI.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker (optional)
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/easyfinance.git
cd easyfinance

# Set up development environment
make setup-dev

# Run the application
make run
```

### Run Tests

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run only unit tests
make test-unit
```

### Code Quality

```bash
# Run all quality checks
make check

# Format code
make format

# Run linting
make lint

# Run security checks
make security
```

## 🏗️ CI/CD Architecture

### Workflow Overview

```mermaid
graph TD
    A[Push/PR] --> B[Pre-commit Hooks]
    B --> C[Code Quality Checks]
    C --> D[Security Scanning]
    D --> E[Unit Tests]
    E --> F[Integration Tests]
    F --> G[Build Package]
    G --> H[Build Docker Image]
    H --> I{Branch?}
    I -->|develop| J[Deploy to Staging]
    I -->|main| K[Deploy to Production]
    I -->|tag| L[Create Release]
    L --> M[Publish to PyPI]
    L --> N[Publish Docker Image]
```

### Pipeline Components

| Component | Description | Triggers |
|-----------|-------------|----------|
| **CI/CD Pipeline** | Main workflow with linting, testing, building | Push, PR to main/develop |
| **Pre-commit** | Code quality hooks | Push, PR to main/develop |
| **CodeQL** | Security analysis | Push, PR, Weekly schedule |
| **Release** | Automated releases | Version tags (v*.*.*) |
| **Dependabot** | Dependency updates | Weekly schedule |

## 🛠️ Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add new feature"  # Pre-commit hooks run automatically

# Push and create PR
git push origin feature/your-feature-name
```

### 2. Code Quality Gates

Every commit goes through:
- **Pre-commit hooks**: Format, lint, type check
- **Automated tests**: Unit and integration tests
- **Security scanning**: Vulnerability and secret detection
- **Code coverage**: Minimum 80% coverage required

### 3. Release Process

```bash
# Create and push version tag
git tag v1.0.0
git push origin v1.0.0

# Automated release process:
# 1. Creates GitHub release
# 2. Publishes to PyPI
# 3. Publishes Docker image
```

## 📊 Quality Metrics

### Code Coverage
- **Target**: 80% minimum coverage
- **Current**: ![Coverage](https://img.shields.io/codecov/c/github/yourusername/easyfinance)
- **Reports**: Available in GitHub Actions artifacts

### Code Quality
- **Linting**: flake8, pylint
- **Formatting**: Black (88 chars)
- **Import sorting**: isort
- **Type checking**: mypy
- **Security**: Bandit, Safety

### Testing
- **Unit tests**: pytest
- **Integration tests**: FastAPI TestClient
- **Test environments**: Python 3.9, 3.10, 3.11
- **Async testing**: pytest-asyncio

## 🔒 Security

### Security Scanning
- **Static analysis**: Bandit for Python security issues
- **Dependency scanning**: Safety for known vulnerabilities
- **Advanced analysis**: GitHub CodeQL
- **Secret detection**: Pre-commit hooks prevent secret commits

### Security Reporting
- **Vulnerabilities**: Reported in GitHub Security tab
- **Security advisories**: Automated through Dependabot
- **Private reporting**: Email security@easyfinance.com for critical issues

## 🐳 Docker

### Build and Run

```bash
# Build Docker image
make docker-build

# Run container
make docker-run

# View logs
make docker-logs

# Stop container
make docker-stop
```

### Docker Hub

Published images are available at:
- `easyfinance/api:latest` - Latest main branch
- `easyfinance/api:v1.0.0` - Specific version tags

## 📦 Package Distribution

### PyPI
- **Package name**: `easyfinance`
- **Installation**: `pip install easyfinance`
- **Automated publishing**: On version tag creation

### GitHub Releases
- **Automated releases**: Created on version tags
- **Artifacts**: Source distribution and wheel files
- **Changelog**: Generated from commit messages

## 🚀 Deployment

### Staging Environment
- **Trigger**: Push to `develop` branch
- **URL**: https://staging.easyfinance.com
- **Purpose**: Testing and validation

### Production Environment
- **Trigger**: Push to `main` branch
- **URL**: https://easyfinance.com
- **Protection**: Requires manual approval

### Environment Configuration

Set up the following secrets in GitHub repository settings:

```bash
# PyPI Publishing
PYPI_API_TOKEN=pypi-...

# Docker Hub
DOCKER_USERNAME=your-username
DOCKER_PASSWORD=your-token

# Deployment (optional)
STAGING_HOST=staging.example.com
STAGING_KEY=-----BEGIN PRIVATE KEY-----...
PRODUCTION_HOST=production.example.com
PRODUCTION_KEY=-----BEGIN PRIVATE KEY-----...
```

## 📈 Monitoring and Observability

### Build Monitoring
- **Build status**: Displayed on repository README
- **Failed builds**: Block pull request merging
- **Notifications**: Email/Slack for build failures

### Performance Monitoring
- **Test execution time**: Tracked in CI logs
- **Build time**: Optimized with caching
- **Coverage trends**: Tracked over time

### Dependency Monitoring
- **Automated updates**: Dependabot creates PRs weekly
- **Security updates**: Prioritized and auto-merged
- **Compatibility testing**: All updates tested in CI

## 🛠️ Available Commands

### Development
```bash
make setup-dev      # Set up development environment
make run           # Run development server
make run-prod      # Run production server
make check         # Run all quality checks
make fix           # Auto-fix formatting issues
```

### Testing
```bash
make test          # Run all tests
make test-cov      # Run tests with coverage
make test-unit     # Run unit tests only
make test-integration  # Run integration tests only
make test-watch    # Run tests in watch mode
```

### Code Quality
```bash
make lint          # Run all linters
make format        # Format code with Black and isort
make format-check  # Check formatting without changes
make security      # Run security scans
make pre-commit    # Run pre-commit hooks
```

### Building
```bash
make build         # Build Python package
make build-wheel   # Build wheel only
make docker-build  # Build Docker image
make clean         # Clean build artifacts
```

### CI/CD
```bash
make ci-lint       # Run CI linting checks
make ci-test       # Run CI tests
make ci-build      # Run CI build process
make ci-full       # Run full CI pipeline locally
```

## 🤝 Contributing

### Getting Started
1. Fork the repository
2. Create a feature branch
3. Set up development environment: `make setup-dev`
4. Make your changes
5. Run quality checks: `make check`
6. Submit a pull request

### Code Style
- **Python**: Follow PEP 8 with Black formatting (88 chars)
- **Imports**: Sorted with isort
- **Type hints**: Required for all public functions
- **Documentation**: Docstrings for all public APIs

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add user authentication
fix: resolve database connection issue
docs: update API documentation
test: add unit tests for user service
```

### Pull Request Process
1. Ensure all CI checks pass
2. Update documentation if needed
3. Add/update tests for new functionality
4. Request review from maintainers
5. Address review feedback

## 📚 Documentation

- **API Documentation**: Available at `/docs` endpoint
- **CI/CD Documentation**: [.github/CICD.md](.github/CICD.md)
- **Contributing Guide**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Security Policy**: [SECURITY.md](SECURITY.md)

## 🐛 Troubleshooting

### Common Issues

**Build failures:**
```bash
# Clean and rebuild
make clean
make ci-full
```

**Test failures:**
```bash
# Run tests in verbose mode
make test -v
```

**Dependency issues:**
```bash
# Update dependencies
make deps-update
```

**Docker issues:**
```bash
# Rebuild Docker image
make docker-stop
make docker-build
make docker-run
```

### Getting Help
- **Issues**: Create a GitHub issue using provided templates
- **Discussions**: Use GitHub Discussions for questions
- **Security**: Email security@easyfinance.com for security issues

## 📊 Project Status

### Build Status
- ✅ Main branch builds passing
- ✅ All tests passing
- ✅ Security scans clean
- ✅ Dependencies up to date

### Recent Activity
- **Last release**: v1.0.0 (2025-06-22)
- **Active branches**: 3
- **Open PRs**: 2
- **Open issues**: 5

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Maintained by**: EasyFinance Team  
**Contact**: team@easyfinance.com  
**Website**: https://easyfinance.com
