"""
EasyFinance Test Suite

This module contains comprehensive unit tests for the EasyFinance application.

Test Structure:
- test_models_*.py: Tests for Pydantic models
- test_auth_*.py: Tests for authentication and authorization
- test_controller_*.py: Tests for database controllers
- test_middleware_*.py: Tests for middleware components
- test_api.py: Tests for API endpoints

Usage:
    Run all tests: pytest
    Run specific test file: pytest tests/test_models_user.py
    Run with coverage: pytest --cov=src
    Run only unit tests: pytest -m unit
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Test metadata
__version__ = "1.0.0"
__author__ = "EasyFinance Development Team"
