from database.db import get_db

class Book:
    def __init__(self, title, author, release_year, available):
        self.title = title
        self.author = author
        self.release_year = release_year
        self.available = available
        
    def __str__(self):
        return f'{self.title} {self.author} {self.release_year} {self.available}'
    
    def borrowBook(self):
        if self.available:
            self.available = False
            return True
        else:
            return False
        
    def returnBook(self):
        if not self.available:
            self.available = True
            return True
        else:
            return False