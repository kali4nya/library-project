from flask import Flask, render_template, request, redirect, url_for, session
from classes.library import Library
from classes.book import Book
from classes.user import User
from config import Config
import json

#flask declaration
app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY

USERS_DIR = Config.USERS_DIR

def load_users():
    with open(USERS_DIR) as f:
        return json.load(f)

USERS = load_users()

#lib initialization
lib = Library()

# testing data
book1 = Book("Harry Potter", "J.K. Rowling", 1997)
book2 = Book("The Hobbit", "J.R.R. Tolkien", 1937)
book3 = Book("The Catcher in the Rye", "J.D. Salinger", 1951)
book4 = Book("Middlesex", "Jeffrey Eugenides", 2002)
book5 = Book("The Dispossessed", "Ursula K. Le Guin", 1974)

# user1 = User("John", "Doe")
# user2 = User("Jane", "Doe")
# user3 = User("Johnathan", "Ddooee")

Library.add_book(lib, [book1, book2, book3, book4, book5])
# Library.add_user(lib, [user1, user2, user3])
#testing data /end

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and USERS[username]["password"] == password:
            if USERS[username]["permission_level"] < 3:
                session['user'] = username  # Store session data
                return redirect(url_for('main'))
            if USERS[username]["permission_level"] == 3:
                session['user'] = username  # Store session data
                return redirect(url_for('adminPanel'))
        else:
            return render_template('home.html', error="Invalid username or password!")

    return render_template('home.html')

@app.route('/main')
def main():
    if 'user' in session:
        username = session['user']
        if username in USERS and USERS[username]['permission_level'] < 3:
            return render_template("main.html")
    return redirect(url_for('home'))

@app.route('/adminPanel')
def adminPanel():
    print(session.get('permission_level'))
    if 'user' in session:
        username = session['user']
        if username in USERS and USERS[username]['permission_level'] == 3:
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
    Library.add_book(lib, book)
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