import pytest
from pydantic import ValidationError

from models.security import Token


class TestToken:
    """Test cases for Token model"""
    
    def test_token_creation(self):
        """Test creating a Token with valid data"""
        token = Token(
            access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test",
            token_type="bearer"
        )
        
        assert token.access_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"
        assert token.token_type == "bearer"

    def test_token_missing_access_token(self):
        """Test that missing access_token raises validation error"""
        with pytest.raises(ValidationError):
            Token(token_type="bearer")

    def test_token_missing_token_type(self):
        """Test that missing token_type raises validation error"""
        with pytest.raises(ValidationError):
            Token(access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test")

    def test_token_empty_access_token(self):
        """Test that empty access_token raises validation error"""
        with pytest.raises(ValidationError):
            Token(access_token="", token_type="bearer")

    def test_token_empty_token_type(self):
        """Test that empty token_type raises validation error"""
        with pytest.raises(ValidationError):
            Token(
                access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test",
                token_type=""
            )

    def test_token_different_token_types(self):
        """Test token with different token types"""
        # Test with different valid token types
        token_types = ["bearer", "Bearer", "JWT", "Basic"]
        
        for token_type in token_types:
            token = Token(
                access_token="test_token_value",
                token_type=token_type
            )
            assert token.token_type == token_type

    def test_token_long_access_token(self):
        """Test token with very long access token"""
        long_token = "a" * 1000
        token = Token(
            access_token=long_token,
            token_type="bearer"
        )
        
        assert token.access_token == long_token

    def test_token_special_characters_in_token(self):
        """Test token with special characters"""
        special_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        
        token = Token(
            access_token=special_token,
            token_type="bearer"
        )
        
        assert token.access_token == special_token
