import sqlite3
import os
from config import Config

def init_db():
    """Initialize the database only if it does not exist."""
    if not os.path.exists(Config.DATABASE_DIRECTORY):
        print("🔧 Database not found. Creating a new one...")
        os.makedirs(os.path.dirname(Config.DATABASE_DIRECTORY), exist_ok=True)
        conn = sqlite3.connect(Config.DATABASE_DIRECTORY)
        
        # Open the schema.sql file in text mode ('r') and specify UTF-8 encoding
        with open("database/schema.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())  # .read() returns a string in UTF-8 encoding
        
        conn.commit()
        conn.close()
        print("✅ Database initialized!")
    else:
        print("⚠️ Database already exists. Skipping initialization.")

if __name__ == "__main__":
    init_db()