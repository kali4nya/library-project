from database.db import get_db
class Book:
    def __init__(self, book_id=None, title=None, author=None, release_year=None, available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.release_year = release_year
        self.available = True
        
    def __str__(self):
        return f'{self.title} by {self.author} ({self.release_year}) - Available: {self.available}'
    
    def save(self):
        """Save the book to the database."""
        db = get_db()
        cursor = db.execute(
            'INSERT INTO books (title, author, release_year, available) VALUES (?, ?, ?, ?)',
            (self.title, self.author, self.release_year, self.available)
        )
        db.commit()
        self.book_id = cursor.lastrowid  # id from sqlite
    
    def update_availability(self, available):
        """Update the book's availability in the database."""
        db = get_db()
        db.execute(
            'UPDATE books SET available = ? WHERE id = ?',
            (available, self.book_id)
        )
        db.commit()
        self.available = available
    
    @staticmethod
    def get_by_id(book_id):
        """Retrieve a book by its ID."""
        db = get_db()
        book = db.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        if book:
            return Book(
                book_id=book['id'],
                title=book['title'],
                author=book['author'],
                release_year=book['release_year'],
                available=bool(book['available'])
            )
        return None