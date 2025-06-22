"""
Test utilities and common fixtures for EasyFinance tests.

This module provides common test utilities, fixtures, and helper functions
that can be used across multiple test files.
"""

import tempfile
import os
import sqlite3
from datetime import date, datetime, timedelta
from typing import Generator, Optional
import bcrypt

from models.user import UserBase, UserData
from models.financial import Expense, FinancialInfo
from controller.sql import Sql


class TestDataFactory:
    """Factory class for creating test data objects"""
    
    @staticmethod
    def create_user(username: str = "testuser", password: str = "testpass123") -> UserBase:
        """Create a test UserBase object"""
        return UserBase(username=username, password=password)
    
    @staticmethod
    def create_user_data(
        username: str = "testuser",
        password: str = "testpass123",
        user_id: int = 1,
        financial_info: Optional[FinancialInfo] = None
    ) -> UserData:
        """Create a test UserData object"""
        if financial_info is None:
            financial_info = FinancialInfo()
        
        return UserData(
            username=username,
            password=password,
            id=user_id,
            financial_info=financial_info
        )
    
    @staticmethod
    def create_expense(
        expense_id: int = 1,
        user_id: int = 1,
        account_id: int = 1,
        category: str = "Food",
        amount: float = 25.50,
        expense_date: Optional[date] = None,
        **kwargs
    ) -> Expense:
        """Create a test Expense object"""
        if expense_date is None:
            expense_date = date.today()
        
        return Expense(
            id=expense_id,
            user_id=user_id,
            account_id=account_id,
            category=category,
            ammount=amount,  # Note: keeping the typo from the original model
            date=expense_date,
            **kwargs
        )
    
    @staticmethod
    def create_financial_info(
        expenses: Optional[list] = None,
        stocks: Optional[list] = None
    ) -> FinancialInfo:
        """Create a test FinancialInfo object"""
        return FinancialInfo(
            expenses=expenses or [],
            stocks=stocks or []
        )


class DatabaseTestHelper:
    """Helper class for database testing"""
    
    @staticmethod
    def create_temp_db() -> str:
        """Create a temporary database file and return its path"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_file.close()
        return temp_file.name
    
    @staticmethod
    def setup_test_database(db_path: str) -> Sql:
        """Set up a test database with necessary tables"""
        sql_db = Sql(db_path)
        
        # Create users table
        sql_db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create expenses table (if needed for future tests)
        sql_db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                account_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                date DATE NOT NULL,
                tags TEXT,
                description TEXT,
                recurring BOOLEAN DEFAULT FALSE,
                due_date DATE,
                currency TEXT,
                location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        sql_db.conn.commit()
        return sql_db
    
    @staticmethod
    def cleanup_db(db_path: str):
        """Clean up temporary database file"""
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    @staticmethod
    def insert_test_user(sql_db: Sql, username: str, password: str) -> int:
        """Insert a test user and return the user ID"""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        sql_db.cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        sql_db.conn.commit()
        
        return sql_db.cursor.lastrowid


class TokenTestHelper:
    """Helper class for JWT token testing"""
    
    @staticmethod
    def create_test_payload(
        username: str = "testuser",
        expires_in_minutes: int = 15,
        **extra_claims
    ) -> dict:
        """Create a test JWT payload"""
        payload = {
            "sub": username,
            "exp": datetime.utcnow() + timedelta(minutes=expires_in_minutes),
            "iat": datetime.utcnow(),
            **extra_claims
        }
        return payload
    
    @staticmethod
    def create_expired_payload(username: str = "testuser", **extra_claims) -> dict:
        """Create an expired JWT payload"""
        payload = {
            "sub": username,
            "exp": datetime.utcnow() - timedelta(minutes=5),
            "iat": datetime.utcnow() - timedelta(minutes=20),
            **extra_claims
        }
        return payload


class MockHelper:
    """Helper class for creating mocks and stubs"""
    
    @staticmethod
    def mock_user_exists_response(exists: bool = False, error: Optional[Exception] = None):
        """Create a mock response for user_exists function"""
        return (exists, error)
    
    @staticmethod
    def mock_create_user_response(error: Optional[Exception] = None):
        """Create a mock response for create_user function"""
        return error
    
    @staticmethod
    def mock_user_login_response(
        success: bool = True,
        error: Optional[str] = None
    ):
        """Create a mock response for user_login function"""
        return (success, error)


class ValidationHelper:
    """Helper class for validation testing"""
    
    @staticmethod
    def assert_user_base_equal(user1: UserBase, user2: UserBase):
        """Assert that two UserBase objects are equal"""
        assert user1.username == user2.username
        assert user1.password == user2.password
    
    @staticmethod
    def assert_expense_equal(expense1: Expense, expense2: Expense):
        """Assert that two Expense objects are equal"""
        assert expense1.id == expense2.id
        assert expense1.user_id == expense2.user_id
        assert expense1.account_id == expense2.account_id
        assert expense1.category == expense2.category
        assert expense1.ammount == expense2.ammount
        assert expense1.date == expense2.date
    
    @staticmethod
    def is_valid_jwt_token(token: str) -> bool:
        """Check if a string looks like a valid JWT token"""
        parts = token.split('.')
        return len(parts) == 3 and all(len(part) > 0 for part in parts)
    
    @staticmethod
    def is_bcrypt_hash(password_hash: bytes) -> bool:
        """Check if a bytes object looks like a bcrypt hash"""
        if not isinstance(password_hash, bytes):
            return False
        try:
            # bcrypt hashes start with $2a$, $2b$, or $2y$
            hash_str = password_hash.decode('utf-8')
            return hash_str.startswith(('$2a$', '$2b$', '$2y$')) and len(hash_str) == 60
        except UnicodeDecodeError:
            return False


# Context managers for testing
class TempDatabaseContext:
    """Context manager for temporary database testing"""
    
    def __init__(self):
        self.db_path = None
        self.sql_db = None
    
    def __enter__(self) -> Sql:
        self.db_path = DatabaseTestHelper.create_temp_db()
        self.sql_db = DatabaseTestHelper.setup_test_database(self.db_path)
        return self.sql_db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.sql_db:
            self.sql_db.conn.close()
        if self.db_path:
            DatabaseTestHelper.cleanup_db(self.db_path)
