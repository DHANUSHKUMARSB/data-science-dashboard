import sqlite3
from functools import wraps
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "employee_events.db"

def with_db_connection(func):
    """
    Decorator that executes the SQL returned by the wrapped function using
    a sqlite3 connection and returns fetched rows.
    The wrapped function should return a SQL string.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            # The wrapped function should return a SQL string
            query = func(*args, **kwargs)
            cursor.execute(query)
            result = cursor.fetchall()
        finally:
            conn.close()
        return result
    return wrapper
