from config import Config

class Library:
    def __init__(self, books = [], users = []):
        self.books = books
        self.users = users
        
    def add_book(self, book):
        self.books.append(book)
        
    def add_user(self, user):
        self.users.append(user)
        
    def borrow_book(self, user, book):
        if book.available and len(user.borrowed_books) <= Config.BORROW_LIMIT:
            user.add_book(book)
            book.available = False
        else:
            return "Book is not available"
        
    def return_book(self, user, book):
        if book in user.borrowed_books:
            user.remove_book(book)
            book.available = True
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