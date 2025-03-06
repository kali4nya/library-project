from database.db import get_db
from classes.book import Book
from classes.user import User
from config import Config

class Library:
    def __init__(self):
        pass
    
    @staticmethod
    def list_all_users():
        """List all registered users in the system."""
        db = get_db()
        users_data = db.execute('SELECT * FROM users').fetchall()
        
        users = []
        for user in users_data:
            users.append(User(user_id=user['id'], name=user['name'], surname=user['surname']))
        
        return users
    
    def list_all_books():
        db = get_db()

        # Fetch all books from the database
        books_data = db.execute('SELECT id, title, author, release_year, available FROM books').fetchall()

        # Using list comprehension with tuple indexing
        books = [
            [book[0], book[1], book[2], book[3], book[4]]
            for book in books_data
        ]

        return books
    
    @staticmethod
    def create_book(title, author, release_year):
        """Create a new book in the library."""
        new_book = Book(title=title, author=author, release_year=release_year)
        new_book.save()
        return new_book
    
    def add_book(user, book_id):
        """Allows user to borrow a book if they haven't exceeded the limit and marks the book as borrowed."""
        db = get_db()

        borrowed_count = db.execute(
            'SELECT COUNT(*) FROM borrowed_books WHERE user_id = ?',
            (user.user_id,)
        ).fetchone()[0]

        if borrowed_count >= Config.BOOK_BORROW_LIMIT:
            print(f"Borrowing limit reached! You cannot borrow more than {Config.BOOK_BORROW_LIMIT} books.")
            return False
        book = Book.get_by_id(book_id)
        if not book:
            print(f"Book with ID {book_id} not found.")
            return False

        if book.available:
            db.execute(
                'UPDATE books SET available = 0 WHERE id = ?',
                (book_id,)
            )
            db.execute(
                'INSERT INTO borrowed_books (user_id, book_id) VALUES (?, ?)',
                (user.user_id, book_id)
            )
            db.commit()
            
            print(f"Book '{book.title}' successfully borrowed by {user.name} {user.surname}.")
            return True

        print(f"Book '{book.title}' is not available for borrowing.")
        return False
    
    def remove_book(user, book_id):
        """Removes a book from the user's borrowed list and marks the book as available."""
        db = get_db()

        book = Book.get_by_id(book_id)
        if not book:
            print(f"Book with ID {book_id} not found.")
            return False

        if not book.available:
            db.execute(
                'UPDATE books SET available = 1 WHERE id = ?',
                (book_id,)
            )
            db.execute(
                'DELETE FROM borrowed_books WHERE user_id = ? AND book_id = ?',
                (user.user_id, book_id)
            )
            db.commit()

            print(f"Book '{book.title}' successfully returned by {user.name} {user.surname}.")
            return True

        print(f"Book '{book.title}' is already available.")
        return False

        
    @staticmethod
    def create_user(name, surname):
        """Create a new user in the system."""
        new_user = User(name=name, surname=surname)
        new_user.save()
        return new_user