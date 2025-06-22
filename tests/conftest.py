import os
import sys
import tempfile
from unittest.mock import MagicMock

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock environment variables for testing
os.environ.setdefault('JWT_SECRET_KEY', 'test-secret-key-for-testing-only')

# Create a temporary database file for testing
TEST_DB_PATH = os.path.join(tempfile.gettempdir(), 'test_easyfinance.db')
