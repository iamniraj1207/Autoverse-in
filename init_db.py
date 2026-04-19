"""
init_db.py - Initialize the AutoVerse database schema using Python's sqlite3.
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "autoverse.db")
schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

if os.path.exists(db_path):
    os.remove(db_path)

con = sqlite3.connect(db_path)
with open(schema_path, "r") as f:
    con.executescript(f.read())

con.close()
print("✓ Database initialized with new schema.")
