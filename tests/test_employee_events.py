import sqlite3
import pytest
from pathlib import Path

# Path to the DB file in your installed package
@pytest.fixture
def db_path():
    return Path(__file__).resolve().parents[1] / "python-package" / "employee_events" / "employee_events.db"

def test_db_exists(db_path):
    assert db_path.exists()

def test_employee_table_exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee'")
    assert cur.fetchone() is not None
    conn.close()

def test_team_table_exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='team'")
    assert cur.fetchone() is not None
    conn.close()

def test_employee_events_table_exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employee_events'")
    assert cur.fetchone() is not None
    conn.close()
