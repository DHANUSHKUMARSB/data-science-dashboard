from pathlib import Path
import sqlite3
import pytest

DB_PATH = Path(__file__).resolve().parents[1] / "python-package" / "employee_events" / "employee_events.db"

@pytest.fixture
def db_path():
    return DB_PATH

def test_db_exists(db_path):
    assert db_path.exists(), "Database file is missing!"

def test_employee_table_exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee';")
    assert cursor.fetchone() is not None
    conn.close()

def test_team_table_exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='team';")
    assert cursor.fetchone() is not None
    conn.close()

def test_employee_events_table_exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee_events';")
    assert cursor.fetchone() is not None
    conn.close()
