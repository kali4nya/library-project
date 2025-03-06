import os

class Config:
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'book_library.db')
