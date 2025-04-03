from config import Config
import json

class User:
    def __init__(self, username, name, surname, password, permission_level = 1):
        self.username = username
        self.name = name
        self.surname = surname
        self.password = password
        self.permission_level = permission_level
        #
        self.borrowed_books = []
        
    def __str__(self):
        return f"{self.username} | {self.name} {self.surname}{(' | Borrowed books: ' +', '.join(self.borrowed_books)) if self.borrowed_books else ''}"
        
    def add_book(self, book):
        self.borrowed_books.append(book.title)
        with open(Config.USERS_DIR, "r", encoding="utf-8") as f:
            users_data = json.load(f)
                
        if self.username in users_data:
            users_data[self.username]["borrowed_books"].append(book.title)
        else:
            print(f"Error: '{self.username}' not found in the database")
            return
        
        with open(Config.USERS_DIR, "w", encoding="utf-8") as f:
            json.dump(users_data, f, indent=4)

    def remove_book(self, book):
        self.borrowed_books.remove(book.title)
        with open(Config.USERS_DIR, "r", encoding="utf-8") as f:
            users_data = json.load(f)
                
        if self.username in users_data:
            users_data[self.username]["borrowed_books"].remove(book.title)
        else:
            print(f"Error: '{self.username}' not found in the database")
            return
        
        with open(Config.USERS_DIR, "w", encoding="utf-8") as f:
            json.dump(users_data, f, indent=4)