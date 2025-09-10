"""
Tests for protocollum core functionality.
"""

import pytest
from pydantic import BaseModel
from protocollum import DataSourceBinding


class TestUser(BaseModel):
    """Test schema for validation."""
    id: int
    name: str
    email: str


class TestDataSourceBinding:
    """Test cases for DataSourceBinding class."""
    
    def test_initialization(self):
        """Test that DataSourceBinding can be initialized with a schema."""
        binding = DataSourceBinding(TestUser)
        assert binding.schema == TestUser
    
    def test_validate_success(self):
        """Test successful data validation."""
        binding = DataSourceBinding(TestUser)
        data = {"id": 1, "name": "Test User", "email": "test@example.com"}
        
        result = binding.validate(data)
        
        assert isinstance(result, TestUser)
        assert result.id == 1
        assert result.name == "Test User"
        assert result.email == "test@example.com"
    
    def test_validate_failure(self):
        """Test validation failure with invalid data."""
        binding = DataSourceBinding(TestUser)
        data = {"id": "invalid", "name": "Test User"}  # Missing email, invalid id
        
        with pytest.raises(Exception):  # Pydantic validation error
            binding.validate(data)
    
    def test_not_implemented_methods(self):
        """Test that placeholder methods raise NotImplementedError."""
        binding = DataSourceBinding(TestUser)
        
        with pytest.raises(NotImplementedError):
            binding.to_sqlalchemy()
        
        with pytest.raises(NotImplementedError):
            binding.to_table()
        
        with pytest.raises(NotImplementedError):
            binding.to_fastapi()