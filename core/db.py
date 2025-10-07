import sqlite3

def setup_demo_db():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE employees(id INT, name TEXT, department TEXT, salary INT)")
    cur.executemany(
        "INSERT INTO employees VALUES (?, ?, ?, ?)",
        [
            (1, "Alice", "Engineering", 100000),
            (2, "Bob", "Engineering", 120000),
            (3, "Charlie", "HR", 90000),
            (4, "Diana", "HR", 95000),
        ],
    )
    conn.commit()
    return conn
