"""
Simple test to verify the test framework is working correctly.
"""
import pytest


def test_basic_functionality():
    """Test that basic Python functionality works"""
    assert 1 + 1 == 2
    assert "hello" == "hello"
    assert [1, 2, 3] == [1, 2, 3]


def test_string_operations():
    """Test string operations"""
    text = "EasyFinance"
    assert text.lower() == "easyfinance"
    assert text.upper() == "EASYFINANCE"
    assert len(text) == 11


def test_list_operations():
    """Test list operations"""
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    assert sum(numbers) == 15
    assert max(numbers) == 5
    assert min(numbers) == 1


@pytest.mark.asyncio
async def test_async_functionality():
    """Test that async functionality works"""
    async def async_add(a, b):
        return a + b
    
    result = await async_add(2, 3)
    assert result == 5


class TestBasicClass:
    """Test class structure"""
    
    def test_class_method(self):
        """Test class method"""
        assert True is True
    
    def test_another_method(self):
        """Test another method"""
        data = {"key": "value"}
        assert data["key"] == "value"
