import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    BORROW_LIMIT = 3
    FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "fallback_secret_key")
    USERS_DIR = "users.json"
    BOOKS_DIR = "books.json"
    ENABLE_AI_BOOK_OVERVIEW = True #will not be enabled without an api key in .env

    BORROW_TIME_ALLOWED = "2 days" #you can use 'minute', 'minutes', 'hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months', 'year', 'years'. SEPERATE NUMBER FROM WORD WITH SINGLE SPACE
    #please use just one example: "2 days" or "5 minutes" or "1 week", DON'T DO "2 hours 20 minutes" DO "140 minutes" INSTEAD (for now at least)
