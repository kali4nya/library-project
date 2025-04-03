from config import Config
import json

class Book:
    def __init__(self, title, author, year, available = True):
        self.title = title
        self.author = author
        self.year = year
        self.available = available
        
    def __str__(self):
        return f"{self.title} by {self.author} ({self.year}), {'available' if self.available else 'not available'}"

    def borrow_book(self):
        self.available = False
        BOOKS_DIR = Config.BOOKS_DIR

        with open(BOOKS_DIR, "r", encoding="utf-8") as f:
            books_data = json.load(f)
            
        if self.title in books_data:
            books_data[self.title]["available"] = False
        else:
            print(f"Error: '{self.title}' not found in the database")
            return
        
        with open(BOOKS_DIR, "w", encoding="utf-8") as f:
            json.dump(books_data, f, indent=4)
    
    def return_book(self):
        self.available = True
        BOOKS_DIR = Config.BOOKS_DIR

        with open(BOOKS_DIR, "r", encoding="utf-8") as f:
            books_data = json.load(f)
            
        if self.title in books_data:
            books_data[self.title]["available"] = True
        else:
            print(f"Error: '{self.title}' not found in the database")
            return
        
        with open(BOOKS_DIR, "w", encoding="utf-8") as f:
            json.dump(books_data, f, indent=4)