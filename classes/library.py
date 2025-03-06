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
        users_data = db.execute('SELECT id, name, surname FROM users').fetchall()
        
        users = []
        for user in users_data:
            users.append(User(user_id=user[0], name=user[1], surname=user[2]))  # Use tuple indexing
        
        return users
    
    def list_all_books():
        """Fetch all books from the database and return them as Book objects."""
        db = get_db()
        books_data = db.execute('SELECT id, title, author, release_year, available FROM books').fetchall()

        books = [Book(book_id=row[0], title=row[1], author=row[2], release_year=row[3], available=row[4]) for row in books_data]
        
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

        # Check if `user` is an ID (string), and if so, fetch the User object from the database
        if isinstance(user, str):  # user is just the ID as string
            user = User.get_by_id(user)  # assuming you have a method to get user by ID

        # Now `user` is an actual User object
        if not user:
            print(f"User not found!")
            return False

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

    def update_book_availability(self, book_id, available):
        """Update the book's availability in the database."""
        db = get_db()
        db.execute(
            'UPDATE books SET available = ? WHERE id = ?',
            (available, book_id)
        )
        db.commit()
        
    @staticmethod
    def create_user(name, surname):
        """Create a new user in the system."""
        new_user = User(name=name, surname=surname)
        new_user.save()
        return new_user