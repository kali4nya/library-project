class Config:
    BORROW_LIMIT = 3
    FLASK_SECRET_KEY = "ooohaverysecretkeyy"
    USERS_DIR = "users.json"
    BOOKS_DIR = "books.json"
    ENABLE_AI_BOOK_OVERVIEW = True #will not be enabled without an api key in openai_API_key.env