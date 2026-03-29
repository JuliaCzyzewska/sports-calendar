import sqlite3
from fastapi import Depends

def get_db():
    conn = sqlite3.connect("data/calendar_data.db")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()