import pytest
from unittest.mock import AsyncMock, MagicMock
from abc import ABC

from controller.databaseI import DbInterface
from models.user import UserBase


class TestDbInterface:
    """Test cases for DbInterface abstract class"""
    
    def test_db_interface_is_abstract(self):
        """Test that DbInterface is an abstract class"""
        assert issubclass(DbInterface, ABC)
        
        # Should not be able to instantiate directly
        with pytest.raises(TypeError):
            DbInterface()

    def test_abstract_methods_exist(self):
        """Test that all required abstract methods are defined"""
        abstract_methods = DbInterface.__abstractmethods__
        expected_methods = {'user_exists', 'register_user', 'user_login'}
        
        assert abstract_methods == expected_methods

    def test_concrete_implementation_required(self):
        """Test that concrete implementation must implement all abstract methods"""
        
        # Incomplete implementation (missing methods)
        class IncompleteDb(DbInterface):
            async def user_exists(self, user: UserBase):
                pass
        
        with pytest.raises(TypeError):
            IncompleteDb()

    def test_complete_implementation_works(self):
        """Test that complete implementation can be instantiated"""
        
        class CompleteDb(DbInterface):
            async def user_exists(self, user: UserBase) -> tuple:
                return True, None
            
            async def register_user(self, user: UserBase) -> tuple:
                return 1, None
            
            async def user_login(self, user: UserBase) -> tuple:
                return 1, None
        
        # Should be able to instantiate
        db = CompleteDb()
        assert isinstance(db, DbInterface)

    def test_method_signatures(self):
        """Test that abstract methods have correct signatures"""
        
        class TestDb(DbInterface):
            async def user_exists(self, user: UserBase) -> tuple:
                return True, None
            
            async def register_user(self, user: UserBase) -> tuple:
                return 1, None
            
            async def user_login(self, user: UserBase) -> tuple:
                return 1, None
        
        db = TestDb()
        
        # Test that methods accept UserBase objects
        user = UserBase(username="test", password="test")
        
        # These should not raise type errors
        assert hasattr(db, 'user_exists')
        assert hasattr(db, 'register_user')
        assert hasattr(db, 'user_login')


class TestDbInterfaceUsage:
    """Test cases for using DbInterface implementations"""
    
    @pytest.fixture
    def mock_db_implementation(self):
        """Create a mock implementation of DbInterface"""
        
        class MockDb(DbInterface):
            def __init__(self):
                self.users = {}
            
            async def user_exists(self, user: UserBase) -> tuple:
                exists = user.username in self.users
                return exists, None
            
            async def register_user(self, user: UserBase) -> tuple:
                if user.username in self.users:
                    return None, Exception("User already exists")
                self.users[user.username] = user
                return 1, None
            
            async def user_login(self, user: UserBase) -> tuple:
                if user.username not in self.users:
                    return None, Exception("User not found")
                stored_user = self.users[user.username]
                if stored_user.password == user.password:
                    return stored_user, None
                return None, Exception("Invalid password")
        
        return MockDb()

    @pytest.mark.asyncio
    async def test_user_exists_flow(self, mock_db_implementation):
        """Test the user_exists method flow"""
        user = UserBase(username="testuser", password="testpass")
        
        # User should not exist initially
        exists, error = await mock_db_implementation.user_exists(user)
        assert exists is False
        assert error is None
        
        # Register user
        await mock_db_implementation.register_user(user)
        
        # User should exist now
        exists, error = await mock_db_implementation.user_exists(user)
        assert exists is True
        assert error is None

    @pytest.mark.asyncio
    async def test_register_user_flow(self, mock_db_implementation):
        """Test the register_user method flow"""
        user = UserBase(username="newuser", password="newpass")
        
        # Should successfully register new user
        result, error = await mock_db_implementation.register_user(user)
        assert result == 1
        assert error is None
        
        # Should fail to register same user again
        result, error = await mock_db_implementation.register_user(user)
        assert result is None
        assert error is not None
        assert "already exists" in str(error)

    @pytest.mark.asyncio
    async def test_user_login_flow(self, mock_db_implementation):
        """Test the user_login method flow"""
        user = UserBase(username="loginuser", password="loginpass")
        
        # Should fail to login non-existent user
        result, error = await mock_db_implementation.user_login(user)
        assert result is None
        assert error is not None
        assert "not found" in str(error)
        
        # Register user first
        await mock_db_implementation.register_user(user)
        
        # Should successfully login with correct credentials
        result, error = await mock_db_implementation.user_login(user)
        assert result is not None
        assert error is None
        assert result.username == user.username
        
        # Should fail with wrong password
        wrong_user = UserBase(username="loginuser", password="wrongpass")
        result, error = await mock_db_implementation.user_login(wrong_user)
        assert result is None
        assert error is not None
        assert "Invalid password" in str(error)
