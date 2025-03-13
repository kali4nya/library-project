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
    
    def return_book(self):
        self.available = True