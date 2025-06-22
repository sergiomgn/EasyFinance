import pytest
from pydantic import ValidationError

from models.user import UserBase, UserData
from models.financial import FinancialInfo


class TestUserBase:
    """Test cases for UserBase model"""
    
    def test_user_base_creation(self):
        """Test creating a UserBase with valid data"""
        user = UserBase(username="testuser", password="testpass123")
        
        assert user.username == "testuser"
        assert user.password == "testpass123"

    def test_user_base_missing_username(self):
        """Test that missing username raises validation error"""
        with pytest.raises(ValidationError):
            UserBase(password="testpass123")

    def test_user_base_missing_password(self):
        """Test that missing password raises validation error"""
        with pytest.raises(ValidationError):
            UserBase(username="testuser")

    def test_user_base_empty_username(self):
        """Test that empty username raises validation error"""
        with pytest.raises(ValidationError):
            UserBase(username="", password="testpass123")

    def test_user_base_empty_password(self):
        """Test that empty password raises validation error"""
        with pytest.raises(ValidationError):
            UserBase(username="testuser", password="")

    def test_user_base_special_characters_username(self):
        """Test username with special characters"""
        user = UserBase(username="test_user@123", password="testpass123")
        assert user.username == "test_user@123"

    def test_user_base_long_credentials(self):
        """Test with long username and password"""
        long_username = "a" * 100
        long_password = "b" * 200
        
        user = UserBase(username=long_username, password=long_password)
        assert user.username == long_username
        assert user.password == long_password


class TestUserData:
    """Test cases for UserData model"""
    
    def test_user_data_creation(self):
        """Test creating UserData with all required fields"""
        financial_info = FinancialInfo()
        
        user_data = UserData(
            username="testuser",
            password="testpass123",
            id=1,
            financial_info=financial_info
        )
        
        assert user_data.username == "testuser"
        assert user_data.password == "testpass123"
        assert user_data.id == 1
        assert user_data.financial_info == financial_info

    def test_user_data_inherits_from_user_base(self):
        """Test that UserData inherits from UserBase"""
        financial_info = FinancialInfo()
        
        user_data = UserData(
            username="testuser",
            password="testpass123",
            id=1,
            financial_info=financial_info
        )
        
        assert isinstance(user_data, UserBase)

    def test_user_data_missing_id(self):
        """Test that missing id raises validation error"""
        financial_info = FinancialInfo()
        
        with pytest.raises(ValidationError):
            UserData(
                username="testuser",
                password="testpass123",
                financial_info=financial_info
            )

    def test_user_data_missing_financial_info(self):
        """Test that missing financial_info raises validation error"""
        with pytest.raises(ValidationError):
            UserData(
                username="testuser",
                password="testpass123",
                id=1
            )

    def test_user_data_invalid_id_type(self):
        """Test that invalid id type raises validation error"""
        financial_info = FinancialInfo()
        
        with pytest.raises(ValidationError):
            UserData(
                username="testuser",
                password="testpass123",
                id="invalid_id",
                financial_info=financial_info
            )
