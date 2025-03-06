from flask import Flask, render_template, request, redirect, url_for, g
import os
from database.db import get_db, close_db
from database.init_db import init_db
from config import Config
from classes.book import Book

app = Flask(__name__)
app.secret_key = "oohhverysecretkey"

app.config["DATABASE"] = Config.DATABASE_DIRECTORY

init_db()
# Ensure database connection is available in Flasks context
@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_appcontext
def teardown_appcontext(exception=None):
    close_db()

@app.route('/')
def home():
    books = Book.get_all_books()
    
    return render_template('index.html', books=books)

@app.route('/create_book', methods=['POST'])
def create_book():
    """Create a new book in the database."""
    title = request.form['title']
    author = request.form['author']
    release_year = request.form['release_year']

    if not release_year:
        return "Release year is required.", 400
    try:
        release_year = int(release_year)
    except ValueError:
        return "Invalid release year. Please enter a valid integer.", 400
    try:
        new_book = Book(title=title, author=author, release_year=release_year)
        new_book.save()
    except ValueError as e:
        return str(e), 400  # If validation fails in the Book class, show the error message

    return redirect(url_for('home'))

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)