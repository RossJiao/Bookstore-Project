import json
import os

def load_books():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'books.json')
    with open(file_path, 'r') as f:
        return json.load(f)

def search_books(keyword, books):
    """Search for books by title or author (case-insensitive)"""
    keyword = keyword.lower()
    results = []
    for book in books:
        if keyword in book['title'].lower() or keyword in book['author'].lower() or keyword in book.get('genre', '').lower():
            results.append(book)
    return results

def display_books(books):
    """Display a list of books in a readable format"""
    if not books:
        print("No books found.")
        return
    print("\n" + "=" * 50)
    for book in books:
        print(f"ID: {book['id']}")
        print(f"Title: {book['title']}")
        print(f"Author: {book['author']}")
        print(f"Price: ${book['price']}")
        print(f"Description: {book['description']}")
        print("-" * 30)
    print("=" * 50)

def main():
    books = load_books()
    print("Welcome to Ross' Bookstore!")
    print("Available books:")
    display_books(books)
    
    while True:
        keyword = input("\nSearch for a book (title/author), or 'quit' to exit: ")
        if keyword.lower() == 'quit':
            break
        results = search_books(keyword, books)
        display_books(results)

if __name__ == "__main__":
    main()