# EasyFinance Makefile
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
SRC_DIR := src
TEST_DIR := tests
VENV_DIR := venv

.PHONY: help install install-dev install-test clean lint format test test-cov build docker run pre-commit setup-dev

help: ## Show this help message
	@echo "EasyFinance Development Commands"
	@echo "================================"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Installation and Setup

install: ## Install production dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r $(SRC_DIR)/requirements.txt

install-dev: ## Install development dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r $(SRC_DIR)/requirements.txt
	$(PIP) install -r $(SRC_DIR)/requirements-dev.txt

install-test: ## Install test dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r $(SRC_DIR)/requirements.txt
	$(PIP) install -r $(TEST_DIR)/requirements-test.txt

install-all: install install-dev install-test ## Install all dependencies

setup-dev: install-all ## Set up development environment
	pre-commit install
	@echo "Development environment setup complete!"

##@ Code Quality

lint: ## Run all linters
	@echo "Running flake8..."
	flake8 $(SRC_DIR) $(TEST_DIR)
	@echo "Running pylint..."
	pylint $(SRC_DIR) --exit-zero
	@echo "Running mypy..."
	mypy $(SRC_DIR) --ignore-missing-imports --no-strict-optional
	@echo "Running bandit..."
	bandit -r $(SRC_DIR)

format: ## Format code with black and isort
	@echo "Running black..."
	black $(SRC_DIR) $(TEST_DIR)
	@echo "Running isort..."
	isort $(SRC_DIR) $(TEST_DIR)

format-check: ## Check code formatting without making changes
	@echo "Checking black formatting..."
	black --check --diff $(SRC_DIR) $(TEST_DIR)
	@echo "Checking isort formatting..."
	isort --check-only --diff $(SRC_DIR) $(TEST_DIR)

security: ## Run security scans
	@echo "Running bandit security scan..."
	bandit -r $(SRC_DIR)
	@echo "Running safety check..."
	safety check

pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

##@ Testing

test: ## Run unit tests
	$(PYTHON) -m pytest $(TEST_DIR) -v

test-cov: ## Run tests with coverage report
	$(PYTHON) -m pytest $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term --cov-report=xml

test-integration: ## Run integration tests only
	$(PYTHON) -m pytest $(TEST_DIR) -v -m integration

test-unit: ## Run unit tests only
	$(PYTHON) -m pytest $(TEST_DIR) -v -m unit

test-watch: ## Run tests in watch mode
	$(PYTHON) -m pytest $(TEST_DIR) -f

##@ Building and Running

build: ## Build the Python package
	$(PYTHON) -m build

build-wheel: ## Build wheel package only
	$(PYTHON) -m build --wheel

clean: ## Clean build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

##@ Docker

docker-build: ## Build Docker image
	docker build -t easyfinance:latest $(SRC_DIR)

docker-run: ## Run Docker container
	docker run -d -p 8000:8000 --name easyfinance easyfinance:latest

docker-stop: ## Stop Docker container
	docker stop easyfinance || true
	docker rm easyfinance || true

docker-logs: ## Show Docker container logs
	docker logs easyfinance

docker-shell: ## Get shell access to running container
	docker exec -it easyfinance /bin/bash

##@ Development

run: ## Run the development server
	cd $(SRC_DIR) && $(PYTHON) -m uvicorn api:app --reload --host 0.0.0.0 --port 8000

run-prod: ## Run the production server
	cd $(SRC_DIR) && $(PYTHON) -m uvicorn api:app --host 0.0.0.0 --port 8000

deps-update: ## Update all dependencies to latest versions
	$(PIP) list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 $(PIP) install -U

deps-check: ## Check for dependency vulnerabilities
	safety check
	$(PIP) audit

##@ CI/CD

ci-lint: format-check lint security ## Run all CI linting checks

ci-test: test-cov ## Run CI tests with coverage

ci-build: clean build docker-build ## Run CI build process

ci-full: ci-lint ci-test ci-build ## Run full CI pipeline locally

##@ Database (for future use)

db-migrate: ## Run database migrations
	@echo "Database migrations not implemented yet"

db-seed: ## Seed database with test data
	@echo "Database seeding not implemented yet"

##@ Documentation

docs-build: ## Build documentation (placeholder)
	@echo "Documentation build not implemented yet"

docs-serve: ## Serve documentation locally (placeholder)
	@echo "Documentation serve not implemented yet"

##@ Environment Management

venv: ## Create virtual environment
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created in $(VENV_DIR)"
	@echo "Activate with: source $(VENV_DIR)/bin/activate"

venv-clean: ## Remove virtual environment
	rm -rf $(VENV_DIR)

##@ Utilities

check: ## Run all quality checks
	@echo "Running all quality checks..."
	$(MAKE) format-check
	$(MAKE) lint
	$(MAKE) security
	$(MAKE) test
	@echo "All checks passed!"

fix: ## Auto-fix code formatting and imports
	$(MAKE) format
	$(MAKE) lint

upgrade: ## Upgrade all tools and dependencies
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install --upgrade -r $(SRC_DIR)/requirements-dev.txt

info: ## Show project information
	@echo "EasyFinance Project Information"
	@echo "==============================="
	@echo "Python version: $$($(PYTHON) --version)"
	@echo "Pip version: $$($(PIP) --version)"
	@echo "Source directory: $(SRC_DIR)"
	@echo "Test directory: $(TEST_DIR)"
	@echo "Virtual environment: $(VENV_DIR)"
	@echo ""
	@echo "Installed packages:"
	@$(PIP) list
