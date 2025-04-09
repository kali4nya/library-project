from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from rapidfuzz import fuzz
from classes.library import Library
from classes.book import Book
from classes.user import User
from config import Config
import json
import os

#flask declaration
app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True

#loading openai API key
openai_API_key = None
ENABLE_AI_BOOK_OVERVIEW = False
try:
    with open("openai_API_key.env", "r") as f:
        openai_API_key = f.read().strip()
except FileNotFoundError:
    print("openai_API_key.env file not found. AI book overview will be disabled.")
if openai_API_key:
    ENABLE_AI_BOOK_OVERVIEW = Config.ENABLE_AI_BOOK_OVERVIEW
#declaring openai model
if ENABLE_AI_BOOK_OVERVIEW:
    model = 'gpt-3.5-turbo' #gpt model
    temperature = 0.65 #keep within 0 - 1 higher values can cause crashing
#end

#custom jinja filters
def split_first(value):
    return str(value).split(',')[0]

app.jinja_env.filters['split_first'] = split_first

def js_escape(value):
    return json.dumps(value)

app.jinja_env.filters['js_escape'] = js_escape
#end

USERS_DIR = Config.USERS_DIR
BOOKS_DIR = Config.BOOKS_DIR

def load_users_list():
    with open(USERS_DIR, "r", encoding="utf-8") as f:
        users_data = json.load(f)

    users = [
        User(
            username,
            data["name"],
            data["surname"],
            data["password"],
            data["permission_level"],
            data.get("borrowed_books", [])  # fallback to empty list if missing
        )
        for username, data in users_data.items()
    ]
    return users

def load_users_dictionary():
    with open(USERS_DIR) as f:
        return json.load(f)

def load_books_list():
    """Loads books from JSON and converts them into Book objects."""
    if not os.path.exists(BOOKS_DIR):
        return []  # If no file exists, return an empty list

    with open(BOOKS_DIR, "r", encoding="utf-8") as f:
        books_data = json.load(f)

    return [Book(title, data["author"], data["year"], data["available"]) for title, data in books_data.items()]

def load_books_dictionary():
    with open(BOOKS_DIR) as f:
        return json.load(f)

#load users
USERSdictionary = load_users_dictionary()
USERSlist = load_users_list()

#load books
BOOKSlist = load_books_list()
BOOKSdictionary = load_books_dictionary()

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
            globals()["USERSdictionary"] = load_users_dictionary()
            globals()["USERSlist"] = load_users_list()
            globals()["BOOKSdictionary"] = load_books_dictionary()
            globals()["BOOKSlist"] = load_books_list()
            user = USERSdictionary[username]
            #chart
            available_books = sum(1 for book in books if book.available)
            unavailable_books = sum(1 for book in books if not book.available)
            chart_data = {
                'labels': ['Available', 'Unavailable'],
                'values': [available_books, unavailable_books]
            }
            #chart end
            return render_template("main.html", books=books, user=user, chart_data=chart_data, ai_overwiew=ENABLE_AI_BOOK_OVERVIEW)
    return redirect(url_for('home'))

@app.route('/search')
def search():
    if 'user' in session:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify([])

        results = []
        
        for title, details in BOOKSdictionary.items():
            combined = f"{title} {details['author']} {details['year']}".lower()
            
            # Exact match check for title, author, and year individually
            title_exact_score = fuzz.ratio(query, title.lower())
            author_exact_score = fuzz.ratio(query, details['author'].lower())
            year_exact_score = fuzz.ratio(query, str(details['year']).lower())
            
            # Add results where any field has an exact match (score 100)
            if title_exact_score == 100 or author_exact_score == 100 or year_exact_score == 100:
                results.append({
                    "title": title,
                    "author": details["author"],
                    "year": details["year"],
                    "available": details["available"],
                    "title_exact_score": title_exact_score,
                    "author_exact_score": author_exact_score,
                    "year_exact_score": year_exact_score,
                    "score": max(title_exact_score, author_exact_score, year_exact_score)  # Take the highest score
                })
            else:
                # Fuzzy match for combined fields if no exact match
                fuzzy_score = fuzz.token_sort_ratio(query, combined)
                if fuzzy_score >= 31:  # Adjust threshold for fuzzy matches
                    results.append({
                        "title": title,
                        "author": details["author"],
                        "year": details["year"],
                        "available": details["available"],
                        "score": fuzzy_score,
                        "title_exact_score": title_exact_score,
                        "author_exact_score": author_exact_score,
                        "year_exact_score": year_exact_score
                    })

        # Sort results based on score, prioritize exact matches
        results.sort(key=lambda x: x['score'], reverse=True)
        return jsonify(results[:5])  # Limit to top 5 results
    return jsonify([])

@app.route('/book_overview', methods=['POST'])
def book_overview():
    if 'user' in session:
        title = request.form.get('title')
        if ENABLE_AI_BOOK_OVERVIEW:
            book = lib.find_book(title)
            if book:
                overview = lib.get_ai_book_overview(book=f"{book.title}, {book.author}, {book.year}", model=model, temperature=temperature, api_key=openai_API_key, ENABLED_AI_BOOK_OVERVIEW=ENABLE_AI_BOOK_OVERVIEW)
                return jsonify({"overview": overview})
        return jsonify({"overview": None})
    return jsonify({"overview": None})

@app.route('/adminPanel')
def adminPanel():
    print(session.get('permission_level'))
    if 'user' in session:
        username = session['user']
        if username in USERSdictionary and USERSdictionary[username]['permission_level'] == 3:
            books = lib.show_books()
            users = lib.show_users()
            #chart
            available_books = sum(1 for book in books if book.available)
            unavailable_books = sum(1 for book in books if not book.available)
            chart_data = {
                'labels': ['Available', 'Unavailable'],
                'values': [available_books, unavailable_books]
            }
            #chart end
            return render_template("adminPanel.html", books=books, users=users, chart_data=chart_data)
    return redirect(url_for('home'))

@app.route('/add_book', methods=['POST'])
def add_book():
    if 'user' in session:
        username = session['user']
        if username in USERSdictionary and USERSdictionary[username]['permission_level'] == 3:
            title = request.form['title']
            author = request.form['author']
            year = request.form['year']
            book = Book(title, author, year)
            lib.add_book(book)
            lib.save_books_to_json(all=False, book=book)
            return redirect(url_for('adminPanel'))
    return redirect(url_for('home'))

@app.route('/add_user', methods=['POST'])
def add_user():
    if 'user' in session:
        username = session['user']
        if username in USERSdictionary and USERSdictionary[username]['permission_level'] == 3:
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
    return redirect(url_for('home'))

@app.route('/borrow_book', methods=['POST'])
def borrow_book():
    if 'user' in session:
        username = session['user']
        if username in USERSdictionary and USERSdictionary[username]['permission_level'] == 3:
            book_title = request.form['title']
            username = request.form['username']
            
            user = lib.find_user(username)
            book = lib.find_book(book_title)
            
            lib.borrow_book(user, book)
            return redirect(url_for('adminPanel'))
        elif username in USERSdictionary and USERSdictionary[username]['permission_level'] < 3:
            book_title = request.form['title']
            
            user = lib.find_user(username)
            book = lib.find_book(book_title)
            
            lib.borrow_book(user, book)
            return redirect(url_for('main'))
    return redirect(url_for('home'))

@app.route('/return_book', methods=['POST'])
def return_book():
    if 'user' in session:
        username = session['user']
        if username in USERSdictionary and USERSdictionary[username]['permission_level'] == 3:
            book_title = request.form['title']
            username = request.form['username']
            
            user = lib.find_user(username)
            book = lib.find_book(book_title)
            
            lib.return_book(user, book)
            return redirect(url_for('adminPanel'))
        elif username in USERSdictionary and USERSdictionary[username]['permission_level'] < 3:
            book_title = request.form['title']
            
            user = lib.find_user(username)
            book = lib.find_book(book_title)
            
            lib.return_book(user, book)
            return redirect(url_for('main'))
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('home'))

#run
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)