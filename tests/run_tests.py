#!/usr/bin/env python3
"""
Simple test runner for EasyFinance using Python's built-in unittest framework.

This runner can be used when pytest has dependency conflicts.
"""
import unittest
import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Mock environment variables for testing
os.environ.setdefault('JWT_SECRET_KEY', 'test-secret-key-for-testing-only')


class TestBasicFunctionality(unittest.TestCase):
    """Basic functionality tests"""
    
    def test_basic_math(self):
        """Test basic math operations"""
        self.assertEqual(1 + 1, 2)
        self.assertEqual(2 * 3, 6)
        self.assertEqual(10 / 2, 5)
    
    def test_string_operations(self):
        """Test string operations"""
        text = "EasyFinance"
        self.assertEqual(text.lower(), "easyfinance")
        self.assertEqual(text.upper(), "EASYFINANCE")
        self.assertEqual(len(text), 11)
    
    def test_list_operations(self):
        """Test list operations"""
        numbers = [1, 2, 3, 4, 5]
        self.assertEqual(len(numbers), 5)
        self.assertEqual(sum(numbers), 15)
        self.assertEqual(max(numbers), 5)
        self.assertEqual(min(numbers), 1)


class TestModelsImport(unittest.TestCase):
    """Test that models can be imported"""
    
    def test_import_user_models(self):
        """Test importing user models"""
        try:
            from models.user import UserBase, UserData
            self.assertTrue(UserBase is not None)
            self.assertTrue(UserData is not None)
        except ImportError as e:
            self.fail(f"Failed to import user models: {e}")
    
    def test_import_financial_models(self):
        """Test importing financial models"""
        try:
            from models.financial import Expense, FinancialInfo, Stock
            self.assertTrue(Expense is not None)
            self.assertTrue(FinancialInfo is not None)
            self.assertTrue(Stock is not None)
        except ImportError as e:
            self.fail(f"Failed to import financial models: {e}")
    
    def test_import_security_models(self):
        """Test importing security models"""
        try:
            from models.security import Token
            self.assertTrue(Token is not None)
        except ImportError as e:
            self.fail(f"Failed to import security models: {e}")


class TestUserBaseModel(unittest.TestCase):
    """Test UserBase model"""
    
    def setUp(self):
        """Set up test fixtures"""
        from models.user import UserBase
        self.UserBase = UserBase
    
    def test_user_base_creation(self):
        """Test creating a UserBase object"""
        user = self.UserBase(username="testuser", password="testpass123")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.password, "testpass123")
    
    def test_user_base_validation(self):
        """Test UserBase validation"""
        # Valid user should create successfully
        user = self.UserBase(username="validuser", password="validpass")
        self.assertIsNotNone(user)
        
        # Test with different usernames and passwords
        test_cases = [
            ("user1", "pass1"),
            ("test_user", "test_pass_123"),
            ("email@example.com", "securepassword"),
        ]
        
        for username, password in test_cases:
            with self.subTest(username=username, password=password):
                user = self.UserBase(username=username, password=password)
                self.assertEqual(user.username, username)
                self.assertEqual(user.password, password)


class TestFinancialModels(unittest.TestCase):
    """Test financial models"""
    
    def setUp(self):
        """Set up test fixtures"""
        from models.financial import Expense, FinancialInfo, Stock
        from datetime import date
        self.Expense = Expense
        self.FinancialInfo = FinancialInfo
        self.Stock = Stock
        self.date = date
    
    def test_stock_creation(self):
        """Test Stock model creation"""
        stock = self.Stock()
        self.assertIsInstance(stock, self.Stock)
    
    def test_expense_creation(self):
        """Test Expense model creation"""
        expense = self.Expense(
            id=1,
            user_id=100,
            account_id=200,
            category="Food",
            ammount=25.50,
            date=self.date(2025, 6, 22)
        )
        
        self.assertEqual(expense.id, 1)
        self.assertEqual(expense.user_id, 100)
        self.assertEqual(expense.account_id, 200)
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.ammount, 25.50)
        self.assertEqual(expense.date, self.date(2025, 6, 22))
    
    def test_financial_info_creation(self):
        """Test FinancialInfo model creation"""
        financial_info = self.FinancialInfo()
        self.assertEqual(financial_info.expenses, [])
        self.assertEqual(financial_info.stocks, [])


class TestDatabaseInterface(unittest.TestCase):
    """Test database interface"""
    
    def test_import_database_interface(self):
        """Test importing database interface"""
        try:
            from controller.databaseI import DbInterface
            self.assertTrue(DbInterface is not None)
        except ImportError as e:
            self.fail(f"Failed to import database interface: {e}")
    
    def test_database_interface_is_abstract(self):
        """Test that DbInterface is abstract"""
        from controller.databaseI import DbInterface
        from abc import ABC
        
        self.assertTrue(issubclass(DbInterface, ABC))
        
        # Should not be able to instantiate directly
        with self.assertRaises(TypeError):
            DbInterface()


def run_tests():
    """Run all tests"""
    # Create test suite
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestBasicFunctionality,
        TestModelsImport,
        TestUserBaseModel,
        TestFinancialModels,
        TestDatabaseInterface,
    ]
    
    for test_class in test_classes:
        tests = test_loader.loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
