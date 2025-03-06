import os

class Config:
    DATABASE_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', 'book_library.db')

    BOOK_BORROW_LIMIT = 3