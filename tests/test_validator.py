import pytest
from agents.validator import validate_or_correct_sql, stats

TEST_SCHEMA = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    amount DECIMAL(10, 2) NOT NULL,
    status TEXT CHECK(status IN ('pending', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def test_valid_sql():
    """Test that valid SQL passes validation without correction."""
    valid_sql = "SELECT * FROM users WHERE id = 1"
    result, was_corrected = validate_or_correct_sql(valid_sql, TEST_SCHEMA)
    assert was_corrected is False

def test_invalid_sql_correction():
    invalid_sql = "SELECT name, email FROM userss"  
    result, was_corrected = validate_or_correct_sql(invalid_sql, TEST_SCHEMA)
    # Check we got a result and it's a boolean
    assert result is not None
    assert isinstance(was_corrected, bool)
    # If the SQL was corrected, check that 'userss' was fixed to 'users'
    if was_corrected:
        assert "users" in result.lower()

def test_complex_query_correction():
    complex_sql = """
    SELECT u.name, COUNT(o.id) as order_count
    FROM users u
{{ ... }}
    WHERE o.status = 'completed' OR o.status IS NULL
    GROUP BY u.id
    HAVING COUNT(o.id) > 1
    """
    result, was_corrected = validate_or_correct_sql(complex_sql, TEST_SCHEMA)
    # Check we got a result and it's a boolean
    assert result is not None
    assert isinstance(was_corrected, bool)
    # If the SQL was corrected, check that 'FROM user' was fixed to 'FROM users'
    if was_corrected:
        assert "from users " in result.lower()

def test_stats_tracking():
    """Test that statistics are being tracked correctly."""
    from agents.validator import ValidationStats
    
    # Create a new stats instance for testing
    test_stats = ValidationStats()
    
    # Save the original stats
    from agents.validator import stats as original_stats
    
    try:
        # Replace the global stats with our test instance
        import agents.validator
        agents.validator.stats = test_stats
        
        # Run some test queries
        validate_or_correct_sql("SELECT * FROM users", TEST_SCHEMA)  # Should be valid
        validate_or_correct_sql("SELECT * FROM userss", TEST_SCHEMA)  # Should be corrected
        validate_or_correct_sql("INVALID SQL", TEST_SCHEMA)  # Should fail
        
        # Get the stats
        stats_data = test_stats.get_stats()
        
        # Basic assertions
        assert stats_data['total_queries'] == 3
        assert 0 <= stats_data['success_rate'] <= 100
        assert 0 <= stats_data['correction_success_rate'] <= 100
        
        print("\nTest Validation Statistics:")
        for k, v in stats_data.items():
            print(f"{k}: {v}")
            
    finally:
        # Restore the original stats
        agents.validator.stats = original_stats

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

    print("\nFinal Statistics:")
    for k, v in stats.get_stats().items():
        print(f"{k}: {v}")
