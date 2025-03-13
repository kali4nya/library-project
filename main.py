from flask import Flask, render_template, request, redirect, url_for
from classes.library import Library
from classes.book import Book
from classes.user import User

#flask declaration
app = Flask(__name__)

#lib initialization
lib = Library()

# testing data
book1 = Book("Harry Potter", "J.K. Rowling", 1997)
book2 = Book("The Hobbit", "J.R.R. Tolkien", 1937)
book3 = Book("The Catcher in the Rye", "J.D. Salinger", 1951)

user1 = User("John", "Doe")
user2 = User("Jane", "Doe")

Library.add_book(lib, [book1, book2, book3])
Library.add_user(lib, [user1, user2])

#testing data /end

@app.route('/')
def index():
    books = lib.show_books()
    users = lib.show_users()
    return render_template("index.html", books=books, users=users)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']
    book = Book(title, author, year)
    Library.add_book(lib, book)
    return redirect(url_for('index'))

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    surname = request.form['surname']
    user = User(name, surname)
    Library.add_user(lib, user)
    return redirect(url_for('index'))

#run
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)