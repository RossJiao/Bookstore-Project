import sqlite3
import json
import os

def init_database():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'bookstore.db')
    json_path = os.path.join(script_dir, 'books.json')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            genre TEXT
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM books')
    if cursor.fetchone()[0] == 0:
        with open(json_path, 'r') as f:
            books = json.load(f)
        for b in books:
            cursor.execute('''
                INSERT INTO books (id, title, author, price, description, genre)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (b['id'], b['title'], b['author'], b['price'], b['description'], b['genre']))
        conn.commit()
        print(f"Inserted {len(books)} books into database.")
    else:
        print("Books already exist in database.")
    
    conn.close()
    print("Database ready: bookstore.db")

if __name__ == "__main__":
    init_database()