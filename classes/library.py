from config import Config
from classes.book import Book
from classes.user import User

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
        if book.available and len(user.borrowed_books) <= Config.BORROW_LIMIT:
            Book.borrow_book(book)
            user.add_book(book)
        else:
            return "Book is not available"
        
    def return_book(self, user, book):
        if book in user.borrowed_books:
            Book.return_book(book)
            user.remove_book(book)
        else:
            return "User has not borrowed this book"
        
    def show_books(self):
        return self.books
    
    def show_users(self):
        return self.users
    
    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return "Book not found"