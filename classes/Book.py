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
    
    def borrow_book(self):
        """Marks the book as borrowed (if available)."""
        if self.available:
            self.update_availability(False)
            return True
        return False
        
    def return_book(self):
        """Marks the book as available (if currently borrowed)."""
        if not self.available:
            self.update_availability(True)
            return True
        return False
    
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
    
    @classmethod
    def get_all_books(cls):
        """Fetch all books from the database and return them as Book objects."""
        db = get_db()
        
        # Fetch all books from the database
        books_data = db.execute('SELECT * FROM books').fetchall()

        # Convert each row (tuple) into a Book object
        books = []
        for book in books_data:
            # Assuming your columns are: id, title, author, release_year, available
            book_id = book[0]
            title = book[1]
            author = book[2]
            release_year = book[3]
            available = book[4]
            
            # Create a Book object for each row and add it to the list
            books.append(cls(book_id=book_id, title=title, author=author, release_year=release_year, available=available))
        
        return books