import sqlite3
from datetime import date


def create_schema(conn: sqlite3.Connection):
    cur = conn.cursor()
    # Enable foreign key enforcement in SQLite
    cur.execute('PRAGMA foreign_keys = ON;')

    # Authors: id PK, full_name
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Authors (
        id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL
    );
    ''')

    # Genres: id PK, name
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Genres (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    ''')

    # Books: id PK, title, year, author_id FK, genre_id FK
    # year has a domain constraint: must be <= current year
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        year INTEGER NOT NULL CHECK(year <= strftime('%Y', 'now')),
        author_id INTEGER NOT NULL,
        genre_id INTEGER NOT NULL,
        FOREIGN KEY(author_id) REFERENCES Authors(id) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY(genre_id) REFERENCES Genres(id) ON DELETE RESTRICT ON UPDATE CASCADE
    );
    ''')

    # Readers: id PK, full_name, email (unique)
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Readers (
        id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    ''')

    # Book_Issues: id PK, book_id FK, reader_id FK, issue_date, return_date (nullable)
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Book_Issues (
        id INTEGER PRIMARY KEY,
        book_id INTEGER NOT NULL,
        reader_id INTEGER NOT NULL,
        issue_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY(book_id) REFERENCES Books(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY(reader_id) REFERENCES Readers(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
    ''')

    conn.commit()


def insert_sample_data(conn: sqlite3.Connection):
    cur = conn.cursor()

    # Insert authors
    authors = [
        (1, 'Isaac Asimov'),
        (2, 'Bjarne Stroustrup'),
        (3, 'Guido van Rossum')
    ]
    cur.executemany('INSERT OR IGNORE INTO Authors(id, full_name) VALUES (?, ?);', authors)

    # Insert genres
    genres = [
        (1, 'Science Fiction'),
        (2, 'Programming'),
        (3, 'Biography')
    ]
    cur.executemany('INSERT OR IGNORE INTO Genres(id, name) VALUES (?, ?);', genres)

    # Insert books
    books = [
        (1, 'Foundation', 1951, 1, 1),
        (2, 'I, Robot', 1950, 1, 1),
        (3, 'The C++ Programming Language', 1985, 2, 2),
        (4, 'Python Tutorial', 1995, 3, 2)
    ]
    cur.executemany('INSERT OR IGNORE INTO Books(id, title, year, author_id, genre_id) VALUES (?, ?, ?, ?, ?);', books)

    # Insert readers
    readers = [
        (1, 'Alice Johnson', 'alice@example.com'),
        (2, 'Bob Smith', 'bob@example.com'),
        (3, 'Carol White', 'carol@example.com')
    ]
    cur.executemany('INSERT OR IGNORE INTO Readers(id, full_name, email) VALUES (?, ?, ?);', readers)

    # Insert book issues: some returned, some not
    today = date.today().isoformat()
    issues = [
        (1, 1, 1, '2025-09-10', '2025-09-20'),  # returned
        (2, 2, 1, '2025-09-22', None),           # not returned
        (3, 3, 2, '2025-09-01', '2025-09-15'),  # returned
        (4, 4, 3, '2025-09-25', None)            # not returned
    ]
    cur.executemany('INSERT OR IGNORE INTO Book_Issues(id, book_id, reader_id, issue_date, return_date) VALUES (?, ?, ?, ?, ?);', issues)

    conn.commit()


def query_all_books_with_author_genre(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute('''
    SELECT b.id, b.title, b.year, a.full_name AS author, g.name AS genre
    FROM Books b
    JOIN Authors a ON b.author_id = a.id
    JOIN Genres g ON b.genre_id = g.id
    ORDER BY b.id;
    ''')
    return cur.fetchall()


def query_readers_with_unreturned_books(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute('''
    SELECT DISTINCT r.id, r.full_name, r.email
    FROM Readers r
    JOIN Book_Issues bi ON r.id = bi.reader_id
    WHERE bi.return_date IS NULL
    ORDER BY r.id;
    ''')
    return cur.fetchall()


def query_count_books_per_author(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute('''
    SELECT a.full_name, COUNT(b.id) AS books_count
    FROM Authors a
    LEFT JOIN Books b ON a.id = b.author_id
    GROUP BY a.id, a.full_name
    ORDER BY books_count DESC, a.full_name;
    ''')
    return cur.fetchall()


def main(db_path: str = ':memory:'):
    # Use a file DB so user can inspect it if needed
    if db_path == ':memory':
        print('Using in-memory database for demo')
    conn = sqlite3.connect(db_path)

    try:
        create_schema(conn)
        insert_sample_data(conn)

        print('\nAll books with authors and genres:')
        for row in query_all_books_with_author_genre(conn):
            print(f'  id={row[0]} title="{row[1]}" year={row[2]} author="{row[3]}" genre="{row[4]}"')

        print('\nReaders currently holding books (not returned):')
        for row in query_readers_with_unreturned_books(conn):
            print(f'  id={row[0]} name="{row[1]}" email={row[2]}')

        print('\nNumber of books per author:')
        for row in query_count_books_per_author(conn):
            print(f'  author="{row[0]}" books_count={row[1]}')

    finally:
        conn.close()


if __name__ == '__main__':
    # Persist DB to a local file so it's easy to inspect; change path if desired
    main(db_path='university.db')
