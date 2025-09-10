#!/usr/bin/env python3
"""
Simple test runner for protocollum without pytest dependency.
"""

import sys
import traceback
from pydantic import BaseModel, ValidationError
from protocollum import DataSourceBinding


class TestUser(BaseModel):
    """Test schema for validation."""
    id: int
    name: str
    email: str


def run_test(test_name, test_func):
    """Run a single test and report result."""
    try:
        test_func()
        print(f"✓ {test_name}")
        return True
    except Exception as e:
        print(f"✗ {test_name}: {e}")
        traceback.print_exc()
        return False


def test_initialization():
    """Test that DataSourceBinding can be initialized with a schema."""
    binding = DataSourceBinding(TestUser)
    assert binding.schema == TestUser


def test_validate_success():
    """Test successful data validation."""
    binding = DataSourceBinding(TestUser)
    data = {"id": 1, "name": "Test User", "email": "test@example.com"}
    
    result = binding.validate(data)
    
    assert isinstance(result, TestUser)
    assert result.id == 1
    assert result.name == "Test User"
    assert result.email == "test@example.com"


def test_validate_failure():
    """Test validation failure with invalid data."""
    binding = DataSourceBinding(TestUser)
    data = {"id": "invalid", "name": "Test User"}  # Missing email, invalid id
    
    try:
        binding.validate(data)
        raise AssertionError("Expected validation to fail")
    except ValidationError:
        pass  # Expected
    except Exception as e:
        raise AssertionError(f"Expected ValidationError, got {type(e)}: {e}")


def test_not_implemented_methods():
    """Test that placeholder methods raise NotImplementedError."""
    binding = DataSourceBinding(TestUser)
    
    try:
        binding.to_sqlalchemy()
        raise AssertionError("Expected NotImplementedError")
    except NotImplementedError:
        pass
    
    try:
        binding.to_table()
        raise AssertionError("Expected NotImplementedError")
    except NotImplementedError:
        pass
    
    try:
        binding.to_fastapi()
        raise AssertionError("Expected NotImplementedError")
    except NotImplementedError:
        pass


def main():
    """Run all tests."""
    tests = [
        ("DataSourceBinding initialization", test_initialization),
        ("Successful validation", test_validate_success),
        ("Validation failure", test_validate_failure),
        ("NotImplementedError methods", test_not_implemented_methods),
    ]
    
    passed = 0
    total = len(tests)
    
    print("Running protocollum tests...\n")
    
    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            passed += 1
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed! ✗")
        return 1


if __name__ == "__main__":
    sys.exit(main())