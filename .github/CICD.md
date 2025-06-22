# CI/CD Pipeline Documentation

This document describes the comprehensive CI/CD pipeline setup for the EasyFinance project.

## Overview

The CI/CD pipeline is built using GitHub Actions and includes the following components:

- **Code Quality**: Linting, formatting, and static analysis
- **Testing**: Unit tests, integration tests, and coverage reporting
- **Security**: Vulnerability scanning and security analysis
- **Building**: Package building and Docker image creation
- **Deployment**: Automated deployment to staging and production
- **Release**: Automated release creation and publishing

## Workflow Files

### 1. Main CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

This is the primary workflow that runs on every push and pull request to main/develop branches.

**Jobs:**
- **lint**: Runs flake8, pylint, and mypy for code quality
- **format**: Checks code formatting with Black and import sorting with isort
- **test**: Runs unit tests across multiple Python versions (3.9, 3.10, 3.11)
- **security**: Runs Bandit and Safety for security scanning
- **build**: Builds Python packages and tests installation
- **docker**: Builds and tests Docker images
- **deploy-staging**: Deploys to staging environment (develop branch only)
- **deploy-production**: Deploys to production environment (main branch only)
- **notification**: Sends build status notifications

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Environment Variables:**
- `PYTHON_VERSION`: Default Python version (3.10)
- `JWT_SECRET_KEY`: Secret key for JWT tokens (test environment)

### 2. Pre-commit Hooks (`.github/workflows/pre-commit.yml`)

Runs pre-commit hooks to ensure code quality before commits.

**Jobs:**
- **pre-commit**: Executes all configured pre-commit hooks

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

### 3. Release Workflow (`.github/workflows/release.yml`)

Handles automated releases when version tags are pushed.

**Jobs:**
- **create-release**: Creates GitHub releases with changelogs
- **publish-pypi**: Publishes packages to PyPI
- **publish-docker**: Publishes Docker images to Docker Hub

**Triggers:**
- Push of version tags (format: `v*.*.*`)

**Required Secrets:**
- `PYPI_API_TOKEN`: PyPI API token for package publishing
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password/token

### 4. CodeQL Security Analysis (`.github/workflows/codeql.yml`)

Performs advanced security analysis using GitHub's CodeQL.

**Jobs:**
- **analyze**: Runs CodeQL analysis for Python code

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` branch
- Weekly schedule (Mondays at 2 AM)

## Configuration Files

### 1. Pre-commit Configuration (`.pre-commit-config.yaml`)

Defines hooks that run before each commit:

- **pre-commit-hooks**: Basic file checks (trailing whitespace, YAML syntax, etc.)
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Code linting
- **mypy**: Type checking
- **bandit**: Security analysis
- **pylint**: Advanced code analysis

### 2. Project Configuration (`pyproject.toml`)

Central configuration file containing:

- **Build system**: setuptools configuration
- **Project metadata**: name, version, dependencies, etc.
- **Tool configurations**: Black, isort, pytest, coverage, mypy, pylint, bandit

### 3. Pytest Configuration (`pytest.ini`)

Test framework configuration:

- Test discovery patterns
- Coverage settings (minimum 80% coverage)
- Async test mode
- Test markers for categorization
- Output formatting

### 4. Dependabot Configuration (`.github/dependabot.yml`)

Automated dependency updates:

- **Python dependencies**: Weekly updates for src/ and tests/
- **GitHub Actions**: Weekly updates for workflow files
- **Docker**: Weekly updates for base images

## Development Workflow

### 1. Local Development

```bash
# Set up development environment
make setup-dev

# Run code quality checks
make check

# Run tests with coverage
make test-cov

# Format code
make format

# Run full CI pipeline locally
make ci-full
```

### 2. Pre-commit Setup

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files
```

### 3. Making Changes

1. Create a feature branch from `develop`
2. Make your changes
3. Run local quality checks: `make check`
4. Commit changes (pre-commit hooks will run automatically)
5. Push branch and create pull request
6. CI pipeline will run automatically

### 4. Release Process

1. Merge changes to `main` branch
2. Create and push a version tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. Release workflow will automatically:
   - Create GitHub release
   - Publish to PyPI
   - Publish Docker image

## Environment Setup

### GitHub Secrets

Configure the following secrets in your GitHub repository:

**Required for releases:**
- `PYPI_API_TOKEN`: PyPI API token for package publishing
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password/access token

**Optional for deployments:**
- `STAGING_HOST`: Staging server hostname
- `STAGING_KEY`: SSH private key for staging deployment
- `PRODUCTION_HOST`: Production server hostname
- `PRODUCTION_KEY`: SSH private key for production deployment

### GitHub Environments

Create the following environments in your repository settings:

**staging:**
- Protection rules: Require review for develop branch deployments
- Environment secrets: staging-specific configurations

**production:**
- Protection rules: Require review for main branch deployments
- Environment secrets: production-specific configurations

**pypi:**
- Protection rules: Require review for PyPI publishing
- Environment secrets: `PYPI_API_TOKEN`

## Quality Gates

The pipeline enforces the following quality gates:

### Code Quality
- **Linting**: flake8 must pass without errors
- **Type checking**: mypy must pass without errors
- **Code complexity**: Maximum complexity of 10 (configurable)
- **Code style**: Black formatting must be applied
- **Import sorting**: isort must be applied

### Testing
- **Unit tests**: All tests must pass
- **Coverage**: Minimum 80% code coverage
- **Multiple Python versions**: Tests must pass on Python 3.9, 3.10, 3.11

### Security
- **Vulnerability scanning**: Bandit security analysis
- **Dependency scanning**: Safety check for known vulnerabilities
- **CodeQL analysis**: Advanced security analysis

### Build
- **Package building**: Python package must build successfully
- **Docker building**: Docker image must build successfully
- **Installation testing**: Package must install correctly

## Monitoring and Notifications

### Build Status
- Build status is displayed on pull requests
- Failed builds prevent merging
- Notification job provides summary of all pipeline results

### Coverage Reports
- Coverage reports are uploaded to Codecov
- HTML coverage reports are generated as artifacts
- Coverage trends are tracked over time

### Security Alerts
- Dependabot creates PRs for security updates
- CodeQL analysis runs weekly
- Security vulnerabilities are reported in GitHub Security tab

## Troubleshooting

### Common Issues

1. **Test failures**: Check test logs and ensure all dependencies are installed
2. **Linting errors**: Run `make format` and `make lint` locally
3. **Coverage below threshold**: Add tests for uncovered code
4. **Docker build failures**: Check Dockerfile and dependencies
5. **Deployment failures**: Verify secrets and environment configurations

### Debugging

1. **Local reproduction**: Use `make ci-full` to run the full pipeline locally
2. **Individual steps**: Run specific make targets (`make lint`, `make test`, etc.)
3. **Debug mode**: Add `ACTIONS_STEP_DEBUG: true` to workflow environment variables
4. **SSH debugging**: Use `tmate` action for interactive debugging sessions

### Performance Optimization

1. **Caching**: Dependencies are cached across workflow runs
2. **Parallel execution**: Independent jobs run in parallel
3. **Matrix builds**: Multiple Python versions tested simultaneously
4. **Conditional execution**: Some jobs only run on specific conditions

## Best Practices

1. **Keep workflows fast**: Use caching and parallel execution
2. **Fail fast**: Run quick checks (linting) before expensive operations (tests)
3. **Security first**: Never expose secrets in logs
4. **Environment consistency**: Use the same Python version across environments
5. **Documentation**: Keep this documentation updated with changes

## Migration from Other CI Systems

If migrating from other CI systems (Jenkins, GitLab CI, etc.):

1. **Secrets migration**: Transfer all secrets to GitHub repository settings
2. **Environment variables**: Update workflow files with new variable names
3. **Deployment scripts**: Adapt deployment commands for GitHub Actions syntax
4. **Notifications**: Configure GitHub notifications or third-party integrations
5. **Artifact storage**: Use GitHub Actions artifacts instead of external storage

## Future Enhancements

Planned improvements to the CI/CD pipeline:

1. **Performance testing**: Add performance benchmarks
2. **Integration testing**: Add end-to-end API tests
3. **Multi-environment deployments**: Support for multiple staging environments
4. **Canary deployments**: Gradual rollout to production
5. **Rollback mechanisms**: Automated rollback on deployment failures
6. **Metrics and monitoring**: Integration with monitoring systems
