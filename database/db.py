import sqlite3
from flask import current_app, g

# connect to the database
def get_db():
    # Use g(flask slang xddd) to store the database connection for the current request
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Enable row access by column name

    return g.db

# closing the connection once the request is done
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()