from flask import Flask, render_template, request, redirect, url_for, session
from classes.library import Library
from classes.book import Book
from classes.user import User
from config import Config
import json
import os

#flask declaration
app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY

USERS_DIR = Config.USERS_DIR
BOOKS_DIR = Config.BOOKS_DIR

def load_users_list():
    with open(USERS_DIR, "r", encoding="utf-8") as f:
        users_data = json.load(f)  # Load JSON as a dictionary

    users = [
        User(username, data["name"], data["surname"], data["password"], data["permission_level"])
        for username, data in users_data.items()
    ]

    return users

def load_users_dictionary():
    with open(USERS_DIR) as f:
        return json.load(f)

USERSdictionary = load_users_dictionary()
USERSlist = load_users_list()

def load_books_list():
    """Loads books from JSON and converts them into Book objects."""
    if not os.path.exists(BOOKS_DIR):
        return []  # If no file exists, return an empty list

    with open(BOOKS_DIR, "r", encoding="utf-8") as f:
        books_data = json.load(f)

    return [Book(title, data["author"], data["year"], data["available"]) for title, data in books_data.items()]

# Load books into a list
BOOKSlist = load_books_list()

#lib initialization
lib = Library()

lib.add_book(BOOKSlist)
lib.add_user(USERSlist)
#end

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == "login":
            username = request.form['username']
            password = request.form['password']
            if username in USERSdictionary and USERSdictionary[username]["password"] == password:
                session['user'] = username  # Store session data
                
                if USERSdictionary[username]["permission_level"] < 3:
                    return redirect(url_for('main'))
                elif USERSdictionary[username]["permission_level"] == 3:
                    return redirect(url_for('adminPanel'))
            else:
                return render_template('home.html', error="Invalid username or password!")

        elif action == "register":
            username = request.form['registerUsername']
            password = request.form['registerPassword'] ###
            name = request.form['registerName']
            surname = request.form['registerSurname']
            if username in USERSdictionary:
                return render_template('home.html', error="Username already exists!")
            # Register the user
            user = User(username=username, name=name, surname=surname, password=password, permission_level=1)
            lib.add_user(user)
            lib.save_users_to_json(all=False, user=user)
            globals()["USERSdictionary"] = load_users_dictionary()
            return render_template('home.html', error="Registration successful! You can now log in.")

    return render_template('home.html')

@app.route('/main')
def main():
    if 'user' in session:
        username = session['user']
        if username in USERSdictionary and USERSdictionary[username]['permission_level'] < 3:
            books = lib.show_books()
            name = USERSdictionary[username]['name']
            return render_template("main.html", books=books, name=name)
    return redirect(url_for('home'))

@app.route('/adminPanel')
def adminPanel():
    print(session.get('permission_level'))
    if 'user' in session:
        username = session['user']
        if username in USERSdictionary and USERSdictionary[username]['permission_level'] == 3:
            books = lib.show_books()
            users = lib.show_users()
            return render_template("adminPanel.html", books=books, users=users)
    return redirect(url_for('home'))

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']
    book = Book(title, author, year)
    lib.add_book(book)
    lib.save_books_to_json(all=False, book=book)
    return redirect(url_for('adminPanel'))

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    name = request.form['name']
    surname = request.form['surname']
    password = request.form['password'] ###
    try:
        permission_level = int(request.form['permission_level'])
    except:
        permission_level = 1
    user = User(username=username, name=name, surname=surname, password=password, permission_level=permission_level)
    lib.add_user(user)
    lib.save_users_to_json(all=False, user=user)
    globals()["USERSdictionary"] = load_users_dictionary()
    return redirect(url_for('adminPanel'))

@app.route('/borrow_book', methods=['POST'])
def borrow_book():
    book_title = request.form['title']
    user_raw = request.form['user_full']
    
    user = lib.find_user(user_raw.split(' ')[0], user_raw.split(' ')[1])
    book = lib.find_book(book_title)
    
    lib.borrow_book(user, book)
    return redirect(url_for('adminPanel'))

@app.route('/return_book', methods=['POST'])
def return_book():
    book_title = request.form['title']
    user_raw = request.form['user_full']
    
    user = lib.find_user(user_raw.split(' ')[0], user_raw.split(' ')[1])
    book = lib.find_book(book_title)
    
    lib.return_book(user, book)
    return redirect(url_for('adminPanel'))

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('home'))

#run
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)