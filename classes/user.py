from classes.book import Book
class User:
    def __init__(self, name, surname, borrowed_books = []):
        self.name = name
        self.surname = surname
        self.borrowed_books = borrowed_books
        
    def __str__(self):
        return f"{self.name} {self.surname}, {self.borrowed_books if self.borrowed_books else 'no borrowed books'}"
        
    def add_book(self, book):
        self.borrowed_books.append(book)
        
    def remove_book(self, book):
        self.borrowed_books.remove(book)
        
    def show_books(self):
        return self.borrowed_books