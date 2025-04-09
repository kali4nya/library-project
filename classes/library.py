from config import Config
from classes.book import Book
from classes.user import User
import json
import os
import requests

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
            if book.available and len(user.borrowed_books) <= Config.BORROW_LIMIT - 1:
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
        # Load books from JSON
        with open(Config.BOOKS_DIR, "r", encoding="utf-8") as f:
            books_data = json.load(f)

        # Update self.books with the latest book data
        self.books = []  # Reset the list before populating it

        for title, details in books_data.items():
            book_entry = Book(title=title, author=details["author"], year=details["year"], available=details["available"])
            self.books.append(book_entry)

        return self.books
    
    def show_users(self):
    # Load users from JSON
        with open(Config.USERS_DIR, "r", encoding="utf-8") as f:
            users_data = json.load(f)

        # Update self.users with the latest user data
        self.users = []  # Reset the list before populating it

        for username, details in users_data.items():
            user_entry = User(username=username, name=details["name"], surname=details["surname"], password=details["password"], permission_level=details["permission_level"])
            user_entry.borrowed_books = details.get("borrowed_books", [])
            self.users.append(user_entry)

        return self.users  # Return the updated user list
    
    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None
    
    def find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def serialize_users(self, user=None, all=True):
        if all:
            return {
                u.username: {
                    "name": u.name,
                    "surname": u.surname,
                    "password": u.password,
                    "permission_level": u.permission_level,
                    "borrowed_books": u.borrowed_books
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
                        "permission_level": u.permission_level,
                        "borrowed_books": u.borrowed_books
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
            
    def serialize_books(self, book=None, all=True):
        if all:
            return {
                b.title: {
                    "author": b.author,
                    "year": b.year,
                    "available": b.available
                }
                for b in self.books
            }

        if book is None:
            raise ValueError("A book must be provided when all=False")

        for b in self.books:
            if b.title == book.title:
                return {
                    b.title: {
                        "author": b.author,
                        "year": b.year,
                        "available": b.available
                    }
                }

        return {}

    def save_books_to_json(self, filename=Config.BOOKS_DIR, all=True, book=None):
        """Saves books to a JSON file without deleting existing books."""

        # Load existing data if the file exists
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {}  # If file is corrupted, start fresh
        else:
            existing_data = {}  # If file doesn't exist, start fresh

        # Get new book data
        new_data = self.serialize_books(book=book, all=all)

        if all:
            # If saving all books, overwrite everything
            existing_data = new_data  
        else:
            # If saving a single book, update only that book's data
            existing_data.update(new_data)  

        # Save updated data back to the file
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(existing_data, file, indent=4)
            print(f"Book data saved to {filename}")
        except Exception as e:
            print(f"Error saving book data: {e}")
            
    def get_ai_book_overview(self, book, model, temperature, api_key, ENABLED_AI_BOOK_OVERVIEW):
        if not ENABLED_AI_BOOK_OVERVIEW:
            return None
        if api_key:
            messages = [
                {"role": "user", "content": "I will give you a book title, the book's author, and the release year of the book. Give me a swift overview of the book(include it's genre)(KEEP IT SHORT):\n" + book}
            ]
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + api_key,
            }
            json_data = {
                'model': model,
                'messages':
                    messages
                ,
                'temperature': temperature,
            }
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
            return response.json()['choices'][0]['message']['content']
