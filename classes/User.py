from database.db import get_db
from config import Config
class User:
    def __init__(self, user_id=None, name=None, surname=None):
        self.user_id = user_id  # ID from sqlite
        self.name = name
        self.surname = surname
        
    def __str__(self):
        return f"{self.name} {self.surname} (ID: {self.user_id})"
    
    def save(self):
        """Save the user to the database. If the user exists, do nothing."""
        db = get_db()
        cursor = db.execute(
            'INSERT INTO users (name, surname) VALUES (?, ?)',
            (self.name, self.surname)
        )
        db.commit()
        self.user_id = cursor.lastrowid  # id from sqlite
        
    def get_by_id(user_id):
        """ Retrieve a user by their ID from the database. """
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if user:
            return User(user_id=user['id'], name=user['name'], surname=user['surname'])
        return None

    def get_borrowed_books(self):
        """Retrieve all borrowed books by the user (only IDs and titles)."""
        db = get_db()
        books = db.execute(
            '''
            SELECT books.id, books.title 
            FROM books
            JOIN borrowed_books ON books.id = borrowed_books.book_id
            WHERE borrowed_books.user_id = ?
            ''', 
            (self.user_id,)
        ).fetchall()
        
        return [{"id": book["id"], "title": book["title"]} for book in books]