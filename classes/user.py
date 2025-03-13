class User:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.borrowed_books = []
        
    def __str__(self):
        return f"{self.name} {self.surname}{(' | Borrowed books: ' +', '.join(self.borrowed_books)) if self.borrowed_books else ''}"
        
    def add_book(self, book):
        self.borrowed_books.append(book.title)

    def remove_book(self, book):
        self.borrowed_books.remove(book.title)