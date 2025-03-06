import sqlite3
import os
from flask import g
from config import Config

def get_db():
    """Establish a database connection."""
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(Config.DATABASE_DIRECTORY)
        
        # Open the schema.sql file in text mode ('r') with UTF-8 encoding to read as string
        with open("database/schema.sql", "r", encoding="utf-8") as f:
            g.db.executescript(f.read())  # Ensure .read() returns a string
        
    return g.db

def close_db(e=None):
    """Close the database connection."""
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()