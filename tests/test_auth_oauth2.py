import pytest
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from jose import jwt, JWTError
from fastapi import HTTPException

from auth.oauth2 import (
    create_token, 
    get_new_refresh_token, 
    SECRET_KEY, 
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)


class TestCreateToken:
    """Test cases for create_token function"""
    
    @pytest.mark.asyncio
    async def test_create_access_token(self):
        """Test creating an access token"""
        data = {"sub": "testuser"}
        token = await create_token(data, "TOKEN")
        
        # Decode the token to verify its contents
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "testuser"
        assert "exp" in decoded
        
        # Verify token expiration is set correctly for access token
        exp_time = datetime.fromtimestamp(decoded["exp"])
        expected_exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # Allow 1 minute tolerance for test execution time
        assert abs((exp_time - expected_exp).total_seconds()) < 60

    @pytest.mark.asyncio
    async def test_create_refresh_token(self):
        """Test creating a refresh token"""
        data = {"sub": "testuser"}
        token = await create_token(data, "REFRESH")
        
        # Decode the token to verify its contents
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "testuser"
        assert "exp" in decoded
        
        # Verify token expiration is set correctly for refresh token
        exp_time = datetime.fromtimestamp(decoded["exp"])
        expected_exp = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        # Allow 1 minute tolerance for test execution time
        assert abs((exp_time - expected_exp).total_seconds()) < 60

    @pytest.mark.asyncio
    async def test_create_token_with_additional_data(self):
        """Test creating token with additional data"""
        data = {"sub": "testuser", "role": "admin", "permissions": ["read", "write"]}
        token = await create_token(data, "TOKEN")
        
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "testuser"
        assert decoded["role"] == "admin"
        assert decoded["permissions"] == ["read", "write"]

    @pytest.mark.asyncio
    async def test_create_token_empty_data(self):
        """Test creating token with empty data"""
        data = {}
        token = await create_token(data, "TOKEN")
        
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in decoded
        # Should only contain expiration time

    @pytest.mark.asyncio
    @patch('auth.oauth2.jwt.encode')
    async def test_create_token_encoding_error(self, mock_encode):
        """Test handling JWT encoding errors"""
        mock_encode.side_effect = Exception("Encoding error")
        
        data = {"sub": "testuser"}
        with pytest.raises(Exception, match="Encoding error"):
            await create_token(data, "TOKEN")


class TestGetNewRefreshToken:
    """Test cases for get_new_refresh_token function"""
    
    @pytest.mark.asyncio
    async def test_get_new_refresh_token_valid(self):
        """Test getting new access token with valid refresh token"""
        # Create a valid refresh token
        data = {"sub": "testuser"}
        refresh_token = jwt.encode(
            {**data, "exp": datetime.utcnow() + timedelta(days=1)},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        
        result = await get_new_refresh_token(refresh_token)
        
        assert "access_token" in result
        assert result["token_type"] == "bearer"
        
        # Verify the new access token contains the correct user
        decoded = jwt.decode(result["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "testuser"

    @pytest.mark.asyncio
    async def test_get_new_refresh_token_expired(self):
        """Test handling expired refresh token"""
        # Create an expired refresh token
        data = {"sub": "testuser"}
        expired_token = jwt.encode(
            {**data, "exp": datetime.utcnow() - timedelta(days=1)},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await get_new_refresh_token(expired_token)
        
        assert exc_info.value.status_code == 401
        assert "Invalid refresh token" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_new_refresh_token_invalid_signature(self):
        """Test handling refresh token with invalid signature"""
        # Create token with wrong secret
        data = {"sub": "testuser"}
        invalid_token = jwt.encode(
            {**data, "exp": datetime.utcnow() + timedelta(days=1)},
            "wrong_secret",
            algorithm=ALGORITHM
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await get_new_refresh_token(invalid_token)
        
        assert exc_info.value.status_code == 401
        assert "Invalid refresh token" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_new_refresh_token_missing_sub(self):
        """Test handling refresh token without 'sub' claim"""
        # Create token without 'sub' claim
        data = {"user_id": "123"}
        token_without_sub = jwt.encode(
            {**data, "exp": datetime.utcnow() + timedelta(days=1)},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await get_new_refresh_token(token_without_sub)
        
        assert exc_info.value.status_code == 401
        assert "Invalid refresh token" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_new_refresh_token_malformed(self):
        """Test handling malformed refresh token"""
        malformed_token = "invalid.token.format"
        
        with pytest.raises(HTTPException) as exc_info:
            await get_new_refresh_token(malformed_token)
        
        assert exc_info.value.status_code == 401
        assert "Invalid refresh token" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_new_refresh_token_empty_string(self):
        """Test handling empty refresh token"""
        with pytest.raises(HTTPException) as exc_info:
            await get_new_refresh_token("")
        
        assert exc_info.value.status_code == 401
        assert "Invalid refresh token" in str(exc_info.value.detail)


class TestConstants:
    """Test OAuth2 constants and configuration"""
    
    def test_secret_key_exists(self):
        """Test that SECRET_KEY is set"""
        assert SECRET_KEY is not None
        assert SECRET_KEY == os.getenv("JWT_SECRET_KEY")

    def test_algorithm_is_hs256(self):
        """Test that ALGORITHM is set to HS256"""
        assert ALGORITHM == "HS256"

    def test_token_expiration_times(self):
        """Test token expiration time constants"""
        assert ACCESS_TOKEN_EXPIRE_MINUTES == 15
        assert REFRESH_TOKEN_EXPIRE_DAYS == 7
        assert isinstance(ACCESS_TOKEN_EXPIRE_MINUTES, int)
        assert isinstance(REFRESH_TOKEN_EXPIRE_DAYS, int)
