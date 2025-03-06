-- Create Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL
);

-- Create Books table
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    release_year INTEGER NOT NULL,
    available BOOLEAN NOT NULL DEFAULT 1
);

-- Create Borrowed Books table (Many-to-Many Relationship)
CREATE TABLE IF NOT EXISTS borrowed_books (
    user_id INTEGER,
    book_id INTEGER,
    PRIMARY KEY (user_id, book_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);