from config import Config
from classes.book import Book
from classes.user import User
import json
import os

class Library:
    def __init__(self, books = [], users = []):
        self.books = books
        self.users = users
        
    def add_book(self, book):
        if type(book) is list:
            for _ in book:
                self.books.append(_)
        elif type(book) is Book:
            self.books.append(book)
        else:    
            return "Invalid input (must be a Book object or a list of Book objects)"
        
    def add_user(self, user):
        if type(user) is list:
            for _ in user:
                self.users.append(_)
        elif type(user) is User:
            self.users.append(user)
        else:
            return "Invalid input (must be a User object or a list of User objects)"
        
    def borrow_book(self, user, book):
        try:
            if book.available and len(user.borrowed_books) <= Config.BORROW_LIMIT:
                book.borrow_book()
                user.add_book(book)
            else:
                return "Book is not available"
        except Exception as e:
            print(f"An error occurred: {e}")
        
    def return_book(self, user, book):
        try:
            if book.title in user.borrowed_books:
                book.return_book()
                user.remove_book(book)
            else:
                print("User has not borrowed this book")
                return "User has not borrowed this book"
        except Exception as e:
            print(f"An error occurred: {e}")
        
    def show_books(self):
        return self.books
    
    def show_users(self):
        return self.users
    
    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return "Book not found"
    
    def find_user(self, user_name, user_surname):
        for user in self.users:
            if user.name.lower() == user_name.lower() and user.surname.lower() == user_surname.lower():
                return user
        return "Book not found"
    
    def serialize_users(self, user=None, all=True):
        if all:
            return {
                u.username: {
                    "name": u.name,
                    "surname": u.surname,
                    "password": u.password,
                    "permission_level": u.permission_level
                }
                for u in self.users
            }

        if user is None:
            raise ValueError("A user must be provided when all=False")

        for u in self.users:
            if u.username == user.username:
                return {
                    u.username: {
                        "name": u.name,
                        "surname": u.surname,
                        "password": u.password,
                        "permission_level": u.permission_level
                    }
                }

        return {}
    
    def save_users_to_json(self, filename=Config.USERS_DIR, all=True, user=None):
        """Saves users to a JSON file without deleting existing users."""

        # Load existing data if the file exists
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {}  # If file is corrupted, start fresh
        else:
            existing_data = {}  # If file doesn't exist, start fresh

        # Get new user data
        new_data = self.serialize_users(user=user, all=all)

        if all:
            # If saving all users, overwrite everything
            existing_data = new_data  
        else:
            # If saving a single user, update only that user's data
            existing_data.update(new_data)  

        # Save updated data back to the file
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(existing_data, file, indent=4)
            print(f"User data saved to {filename}")
        except Exception as e:
            print(f"Error saving user data: {e}")