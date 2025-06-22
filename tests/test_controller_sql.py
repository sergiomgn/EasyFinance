import pytest
import sqlite3
import tempfile
import os
from unittest.mock import patch, MagicMock
import bcrypt

from controller.sql import Sql
from models.user import UserBase


class TestSqlInit:
    """Test cases for Sql class initialization"""
    
    def test_sql_init_creates_connection(self):
        """Test that Sql initialization creates database connection"""
        with tempfile.NamedTemporaryFile(delete=False) as temp_db:
            db_name = temp_db.name
        
        try:
            sql_db = Sql(db_name)
            assert sql_db.conn is not None
            assert sql_db.cursor is not None
            assert isinstance(sql_db.conn, sqlite3.Connection)
            assert isinstance(sql_db.cursor, sqlite3.Cursor)
        finally:
            os.unlink(db_name)

    def test_sql_init_in_memory_db(self):
        """Test initialization with in-memory database"""
        sql_db = Sql(":memory:")
        assert sql_db.conn is not None
        assert sql_db.cursor is not None


class TestSqlUserExists:
    """Test cases for user_exists method"""
    
    @pytest.fixture
    def sql_db(self):
        """Create SQL database instance for testing"""
        db = Sql(":memory:")
        # Create users table for testing
        db.cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        db.conn.commit()
        return db

    @pytest.mark.asyncio
    async def test_user_exists_returns_false_when_user_not_found(self, sql_db):
        """Test user_exists returns False when user doesn't exist"""
        user = UserBase(username="nonexistent", password="password")
        
        exists, error = await sql_db.user_exists(user)
        
        assert exists is False
        assert error is None

    @pytest.mark.asyncio
    async def test_user_exists_returns_true_when_user_found(self, sql_db):
        """Test user_exists returns True when user exists"""
        # Insert a user manually
        sql_db.cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("testuser", "hashedpassword")
        )
        sql_db.conn.commit()
        
        user = UserBase(username="testuser", password="password")
        exists, error = await sql_db.user_exists(user)
        
        assert exists is True
        assert error is None

    @pytest.mark.asyncio
    async def test_user_exists_handles_database_error(self, sql_db):
        """Test user_exists handles database errors gracefully"""
        # Close the connection to simulate an error
        sql_db.conn.close()
        
        user = UserBase(username="testuser", password="password")
        exists, error = await sql_db.user_exists(user)
        
        assert exists is None
        assert error is not None
        assert isinstance(error, Exception)


class TestSqlCreateUser:
    """Test cases for create_user method"""
    
    @pytest.fixture
    def sql_db(self):
        """Create SQL database instance for testing"""
        db = Sql(":memory:")
        # Create users table for testing
        db.cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        db.conn.commit()
        return db

    @pytest.mark.asyncio
    async def test_create_user_success(self, sql_db):
        """Test successful user creation"""
        user = UserBase(username="newuser", password="plainpassword")
        
        error = await sql_db.create_user(user)
        
        assert error is None
        
        # Verify user was created and password was hashed
        sql_db.cursor.execute("SELECT username, password FROM users WHERE username = ?", ("newuser",))
        result = sql_db.cursor.fetchone()
        
        assert result is not None
        assert result[0] == "newuser"
        # Password should be hashed (bcrypt hash)
        assert result[1] != "plainpassword"
        assert isinstance(result[1], bytes)  # bcrypt returns bytes

    @pytest.mark.asyncio
    async def test_create_user_password_hashing(self, sql_db):
        """Test that password is properly hashed with bcrypt"""
        user = UserBase(username="hashtest", password="testpassword123")
        
        await sql_db.create_user(user)
        
        # Get the stored password
        sql_db.cursor.execute("SELECT password FROM users WHERE username = ?", ("hashtest",))
        result = sql_db.cursor.fetchone()
        stored_password = result[0]
        
        # Verify the password can be checked with bcrypt
        assert bcrypt.checkpw("testpassword123".encode('utf-8'), stored_password)
        assert not bcrypt.checkpw("wrongpassword".encode('utf-8'), stored_password)

    @pytest.mark.asyncio
    async def test_create_user_duplicate_username(self, sql_db):
        """Test creating user with duplicate username"""
        user1 = UserBase(username="duplicate", password="password1")
        user2 = UserBase(username="duplicate", password="password2")
        
        # Create first user
        error1 = await sql_db.create_user(user1)
        assert error1 is None
        
        # Try to create second user with same username
        error2 = await sql_db.create_user(user2)
        assert error2 is not None
        assert isinstance(error2, Exception)

    @pytest.mark.asyncio
    async def test_create_user_handles_database_error(self, sql_db):
        """Test create_user handles database errors"""
        # Close connection to simulate error
        sql_db.conn.close()
        
        user = UserBase(username="erroruser", password="password")
        error = await sql_db.create_user(user)
        
        assert error is not None
        assert isinstance(error, Exception)


class TestSqlUserLogin:
    """Test cases for user_login method"""
    
    @pytest.fixture
    def sql_db_with_user(self):
        """Create SQL database with a test user"""
        db = Sql(":memory:")
        # Create users table
        db.cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        db.conn.commit()
        
        # Create a test user with hashed password
        test_password = "testpassword123"
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(test_password.encode('utf-8'), salt)
        
        db.cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("testuser", hashed_password)
        )
        db.conn.commit()
        
        return db

    @pytest.mark.asyncio
    async def test_user_login_success(self, sql_db_with_user):
        """Test successful user login"""
        user = UserBase(username="testuser", password="testpassword123")
        
        success, error = await sql_db_with_user.user_login(user)
        
        assert success is True
        assert error is None

    @pytest.mark.asyncio
    async def test_user_login_user_not_found(self, sql_db_with_user):
        """Test login with non-existent user"""
        user = UserBase(username="nonexistent", password="password")
        
        success, error = await sql_db_with_user.user_login(user)
        
        assert success is False
        assert error == "User not found"

    @pytest.mark.asyncio
    async def test_user_login_invalid_password(self, sql_db_with_user):
        """Test login with invalid password"""
        user = UserBase(username="testuser", password="wrongpassword")
        
        success, error = await sql_db_with_user.user_login(user)
        
        assert success is False
        assert error == "Invalid password"

    @pytest.mark.asyncio
    async def test_user_login_handles_database_error(self, sql_db_with_user):
        """Test user_login handles database errors"""
        # Close connection to simulate error
        sql_db_with_user.conn.close()
        
        user = UserBase(username="testuser", password="testpassword123")
        success, error = await sql_db_with_user.user_login(user)
        
        assert success is False
        assert error is not None
        assert isinstance(error, str)


class TestSqlIntegration:
    """Integration tests for Sql class"""
    
    @pytest.fixture
    def sql_db(self):
        """Create SQL database instance for integration testing"""
        db = Sql(":memory:")
        # Create users table
        db.cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        db.conn.commit()
        return db

    @pytest.mark.asyncio
    async def test_full_user_lifecycle(self, sql_db):
        """Test complete user lifecycle: check exists, create, login"""
        user = UserBase(username="lifecycle_user", password="password123")
        
        # 1. User should not exist initially
        exists, error = await sql_db.user_exists(user)
        assert exists is False
        assert error is None
        
        # 2. Create the user
        error = await sql_db.create_user(user)
        assert error is None
        
        # 3. User should now exist
        exists, error = await sql_db.user_exists(user)
        assert exists is True
        assert error is None
        
        # 4. Should be able to login
        success, error = await sql_db.user_login(user)
        assert success is True
        assert error is None
        
        # 5. Should not be able to login with wrong password
        wrong_user = UserBase(username="lifecycle_user", password="wrongpassword")
        success, error = await sql_db.user_login(wrong_user)
        assert success is False
        assert error == "Invalid password"
