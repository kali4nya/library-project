from flask import Flask, render_template, request, redirect, url_for, g
import os
from database.db import get_db, close_db
from database.init_db import init_db
from config import Config
from classes.book import Book
from classes.user import User
from classes.library import Library

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
    books = Library.list_all_books()
    users = Library.list_all_users()
    return render_template('index.html', books=books, users=users)

@app.route('/create_book', methods=['POST'])
def create_book():
    title = request.form['title']
    author = request.form['author']
    release_year = int(request.form['release_year'])
    
    new_book = Book(title=title, author=author, release_year=release_year)
    new_book.save()

    return redirect(url_for('home'))

@app.route('/create_user', methods=['POST'])
def create_user():
    name = request.form['name']
    surname = request.form['surname']
    
    # Create the user and save to the database
    new_user = User(name=name, surname=surname)
    new_user.save()
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)