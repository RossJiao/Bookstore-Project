import sqlite3
import os

def get_db_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bookstore.db')

def search_books(keyword):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    keyword = f'%{keyword}%'
    cursor.execute('''
        SELECT id, title, author, price, description, genre
        FROM books
        WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?
    ''', (keyword, keyword, keyword))
    
    results = cursor.fetchall()
    conn.close()
    return results

def display_books(books):
    if not books:
        print("No books found.")
        return
    print("\n" + "=" * 50)
    for book in books:
        print(f"ID: {book[0]}")
        print(f"Title: {book[1]}")
        print(f"Author: {book[2]}")
        print(f"Price: ${book[3]}")
        print(f"Description: {book[4]}")
        print(f"Genre: {book[5]}")
        print("-" * 30)
    print("=" * 50)

def main():
    print("Welcome to Ross' Bookstore!")
    while True:
        keyword = input("\nSearch for a book (title/author/genre), or 'quit' to exit: ")
        if keyword.lower() == 'quit':
            break
        results = search_books(keyword)
        display_books(results)

if __name__ == "__main__":
    main()