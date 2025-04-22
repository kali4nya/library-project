from config import Config
import json
import time
import hashlib
from utils import update_json_file

class User:
    def __init__(self, username, name, surname, password, permission_level=1, borrowed_books=None):
        self.username = username
        self.name = name
        self.surname = surname
        self.password = password  # Password should already be hashed from client-side
        self.permission_level = permission_level
        self.borrowed_books = borrowed_books if borrowed_books is not None else []

    def verify_password(self, password_to_check):
        """
        Verify if the provided password matches the stored password hash.
        Since passwords are hashed on the client side, this just compares the hashes.
        """
        return self.password == password_to_check

    def __str__(self):
        if not self.borrowed_books:
            return f"{self.username} | {self.name} {self.surname}"

        # Extract titles and borrow times from borrowed_books (which may contain dictionaries or strings)
        book_details = []
        for book in self.borrowed_books:
            if isinstance(book, dict):
                title = book.get('title', 'Unknown')
                borrow_time = book.get('borrow_time', None)
                if borrow_time:
                    # Format the timestamp as a readable date string
                    from datetime import datetime
                    borrow_date = datetime.fromtimestamp(borrow_time).strftime('%Y-%m-%d %H:%M:%S')
                    book_details.append(f"{title} (borrowed at: {borrow_date})")
                else:
                    book_details.append(title)
            else:
                book_details.append(str(book))

        return f"{self.username} | {self.name} {self.surname} | Borrowed books: {', '.join(book_details)}"

    def add_book(self, book):
        """Add a book to the user's borrowed books list and update the JSON file."""
        # Create book info with borrow time
        book_title = book.title
        borrow_time = int(time.time())
        borrow_info = {
            "title": book_title,
            "borrow_time": borrow_time
        }

        # Add to the in-memory list
        self.borrowed_books.append(borrow_info)

        # Define the update function
        def update_borrowed_books(user_data):
            if "borrowed_books" not in user_data:
                user_data["borrowed_books"] = []

            # Add the same book info to JSON
            user_data["borrowed_books"].append(borrow_info)

        # Update the JSON file
        success = update_json_file(Config.USERS_DIR, self.username, update_borrowed_books)
        if not success:
            # Revert the change if the update failed
            self.borrowed_books.pop()  # Remove the last added book
            return False
        return True

    def remove_book(self, book):
        """Remove a book from the user's borrowed books list and update the JSON file."""
        # Remove from the in-memory list
        book_title = book.title

        # Check if the book is in the borrowed_books list
        # The list might contain strings or dictionaries
        book_found = False
        book_index = -1

        for i, borrowed_book in enumerate(self.borrowed_books):
            if isinstance(borrowed_book, dict) and borrowed_book.get('title') == book_title:
                book_found = True
                book_index = i
                break
            elif borrowed_book == book_title:
                book_found = True
                book_index = i
                break

        if book_found:
            self.borrowed_books.pop(book_index)
        else:
            print(f"Book '{book_title}' not in user's borrowed books")
            return False

        # Define the update function
        def update_borrowed_books(user_data):
            if "borrowed_books" not in user_data:
                user_data["borrowed_books"] = []
                return

            # Find and remove the book
            for i, book_info in enumerate(user_data["borrowed_books"]):
                if isinstance(book_info, dict) and book_info.get("title") == book_title:
                    user_data["borrowed_books"].pop(i)
                    return
                elif isinstance(book_info, str) and book_info == book_title:
                    user_data["borrowed_books"].pop(i)
                    return

        # Update the JSON file
        success = update_json_file(Config.USERS_DIR, self.username, update_borrowed_books)
        if not success:
            # Revert the change if the update failed
            self.borrowed_books.append(book_title)
            return False
        return True
