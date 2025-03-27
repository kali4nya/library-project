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
        return f"{self.name} {self.surname}{(' | Borrowed books: ' +', '.join(self.borrowed_books)) if self.borrowed_books else ''}"
        
    def add_book(self, book):
        self.borrowed_books.append(book.title)

    def remove_book(self, book):
        self.borrowed_books.remove(book.title)