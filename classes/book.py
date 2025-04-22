from config import Config
import json
from utils import update_json_file

class Book:
    def __init__(self, title, author, year, available = True):
        self.title = title
        self.author = author
        # Ensure year is stored as an integer
        try:
            self.year = int(year)
        except (ValueError, TypeError):
            # If conversion fails, store as is but log a warning
            print(f"Warning: Year '{year}' for book '{title}' could not be converted to an integer")
            self.year = year
        self.available = available

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year}), {'available' if self.available else 'not available'}"

    def borrow_book(self):
        """Mark the book as borrowed and update the JSON file."""
        self.available = False

        # Define the update function
        def update_book_availability(book_data):
            book_data["available"] = False

        # Update the JSON file
        success = update_json_file(Config.BOOKS_DIR, self.title, update_book_availability)
        if not success:
            # Revert the change if the update failed
            self.available = True
            return False
        return True

    def return_book(self):
        """Mark the book as returned and update the JSON file."""
        self.available = True

        # Define the update function
        def update_book_availability(book_data):
            book_data["available"] = True

        # Update the JSON file
        success = update_json_file(Config.BOOKS_DIR, self.title, update_book_availability)
        if not success:
            # Revert the change if the update failed
            self.available = False
            return False
        return True
