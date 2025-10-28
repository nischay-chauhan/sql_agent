import sqlite3
import os
from pathlib import Path

# Use a file-based database in the project root
DB_PATH = os.path.join(Path(__file__).parent.parent, "sqlbot.db")

def get_db_connection():
    """Get a connection to the SQLite database, creating it if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def setup_demo_db():
    """Initialize the database with the required tables and sample data."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            salary INTEGER
        )
    """)
    
    # Insert sample data into employees (only if the table is empty)
    cursor.execute("SELECT COUNT(*) as count FROM employees")
    if cursor.fetchone()['count'] == 0:
        cursor.executemany(
            "INSERT INTO employees (id, name, department, salary) VALUES (?, ?, ?, ?)",
            [
                (1, "Alice", "Engineering", 100000),
                (2, "Bob", "Engineering", 120000),
                (3, "Charlie", "HR", 90000),
                (4, "Diana", "HR", 95000),
            ],
        )
    
    conn.commit()
    return conn