import pytest
from datetime import date
from typing import List

from models.financial import Stock, Expense, FinancialInfo


class TestStock:
    """Test cases for Stock model"""
    
    def test_stock_creation(self):
        """Test that Stock model can be created"""
        stock = Stock()
        assert isinstance(stock, Stock)


class TestExpense:
    """Test cases for Expense model"""
    
    def test_expense_creation_with_required_fields(self):
        """Test creating an expense with all required fields"""
        expense = Expense(
            id=1,
            user_id=100,
            account_id=200,
            category="Food",
            ammount=25.50,
            date=date(2025, 6, 22)
        )
        
        assert expense.id == 1
        assert expense.user_id == 100
        assert expense.account_id == 200
        assert expense.category == "Food"
        assert expense.ammount == 25.50
        assert expense.date == date(2025, 6, 22)
        assert expense.tags == []
        assert expense.description == ""
        assert expense.recurring is False
        assert expense.due_date is None
        assert expense.currency is None
        assert expense.location is None

    def test_expense_creation_with_all_fields(self):
        """Test creating an expense with all fields"""
        expense = Expense(
            id=1,
            user_id=100,
            account_id=200,
            category="Food",
            ammount=25.50,
            date=date(2025, 6, 22),
            tags=["restaurant", "lunch"],
            description="Lunch at local restaurant",
            recurring=True,
            due_date=date(2025, 6, 30),
            currency="USD",
            location="Downtown"
        )
        
        assert expense.tags == ["restaurant", "lunch"]
        assert expense.description == "Lunch at local restaurant"
        assert expense.recurring is True
        assert expense.due_date == date(2025, 6, 30)
        assert expense.currency == "USD"
        assert expense.location == "Downtown"

    def test_expense_invalid_data(self):
        """Test that invalid data raises validation errors"""
        with pytest.raises(Exception):
            Expense(
                id="invalid",  # Should be int
                user_id=100,
                account_id=200,
                category="Food",
                ammount=25.50,
                date=date(2025, 6, 22)
            )


class TestFinancialInfo:
    """Test cases for FinancialInfo model"""
    
    def test_financial_info_creation_empty(self):
        """Test creating empty financial info"""
        financial_info = FinancialInfo()
        
        assert financial_info.expenses == []
        assert financial_info.stocks == []

    def test_financial_info_creation_with_data(self):
        """Test creating financial info with data"""
        expense = Expense(
            id=1,
            user_id=100,
            account_id=200,
            category="Food",
            ammount=25.50,
            date=date(2025, 6, 22)
        )
        stock = Stock()
        
        financial_info = FinancialInfo(
            expenses=[expense],
            stocks=[stock]
        )
        
        assert len(financial_info.expenses) == 1
        assert len(financial_info.stocks) == 1
        assert financial_info.expenses[0] == expense
        assert financial_info.stocks[0] == stock

    def test_financial_info_add_expense(self):
        """Test adding expenses to financial info"""
        financial_info = FinancialInfo()
        expense = Expense(
            id=1,
            user_id=100,
            account_id=200,
            category="Food",
            ammount=25.50,
            date=date(2025, 6, 22)
        )
        
        financial_info.expenses.append(expense)
        
        assert len(financial_info.expenses) == 1
        assert financial_info.expenses[0] == expense
