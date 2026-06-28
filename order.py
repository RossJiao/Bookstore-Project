import sqlite3
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Email configuration - REPLACE WITH YOUR OWN
EMAIL_SENDER = "rossjiao122@gmail.com"
EMAIL_PASSWORD = "gnhxztuocekbocin"
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587

def get_db_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bookstore.db')

def get_books():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, author, price FROM books')
    books = cursor.fetchall()
    conn.close()
    return books

def get_book_by_id(book_id):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, author, price FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()
    return book

def save_order(order):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    # Create orders table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            user_name TEXT NOT NULL,
            user_email TEXT NOT NULL,
            book_id INTEGER,
            book_title TEXT,
            book_author TEXT,
            quantity INTEGER,
            unit_price REAL,
            total_price REAL,
            order_date TEXT,
            status TEXT
        )
    ''')
    
    cursor.execute('''
        INSERT INTO orders (
            order_id, user_name, user_email, book_id, book_title, book_author,
            quantity, unit_price, total_price, order_date, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order['order_id'], order['user_name'], order['user_email'],
        order['book_id'], order['book_title'], order['book_author'],
        order['quantity'], order['unit_price'], order['total_price'],
        order['order_date'], order['status']
    ))
    
    conn.commit()
    conn.close()

def generate_order_id():
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    # Create orders table if it doesn't exist (for the count query)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            user_name TEXT NOT NULL,
            user_email TEXT NOT NULL,
            book_id INTEGER,
            book_title TEXT,
            book_author TEXT,
            quantity INTEGER,
            unit_price REAL,
            total_price REAL,
            order_date TEXT,
            status TEXT
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM orders WHERE order_id LIKE ?', (f'ORD-{date_str}%',))
    count = cursor.fetchone()[0]
    conn.close()
    return f"ORD-{date_str}-{count + 1:04d}"

def generate_ebook_placeholder(order):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    orders_dir = os.path.join(script_dir, 'orders')
    if not os.path.exists(orders_dir):
        os.makedirs(orders_dir)
    
    filename = f"{order['order_id']}.txt"
    file_path = os.path.join(orders_dir, filename)
    
    content = f"""
========================================
EBOOK PLACEHOLDER
========================================
Order ID: {order['order_id']}
Book: {order['book_title']}
Author: {order['book_author']}
User: {order['user_name']}
Email: {order['user_email']}
Order Date: {order['order_date']}
========================================
This is a placeholder file for your eBook.
The actual eBook will be available for download at:
https://bookstore.example.com/download/{order['order_id']}
========================================
"""
    
    with open(file_path, 'w') as f:
        f.write(content.strip())
    
    return file_path

def send_order_email(order, ebook_file_path):
    subject = f"Bookstore Order Confirmation - {order['order_id']}"
    
    body = f"""
Dear {order['user_name']},

Thank you for your order at Ross' Bookstore!

Order Details:
----------------------------------------
Order ID: {order['order_id']}
Book: {order['book_title']}
Author: {order['book_author']}
Quantity: {order['quantity']}
Total: ${order['total_price']}
Order Date: {order['order_date']}
----------------------------------------

Your eBook placeholder is attached to this email.
You can also download your eBook using the link below:
https://bookstore.example.com/download/{order['order_id']}

If you have any questions, please reply to this email.

Best regards,
Ross' Bookstore
"""
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = order['user_email']
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with open(ebook_file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            filename = os.path.basename(ebook_file_path)
            part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            msg.attach(part)
    except Exception as e:
        print(f"Warning: Could not attach file: {e}")
    
    try:
        server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {order['user_email']}")
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False

def create_order():
    books = get_books()
    
    print("\n" + "=" * 50)
    print("Place an Order")
    print("=" * 50)
    
    print("\nAvailable Books:")
    for book in books:
        print(f"  {book[0]}. {book[1]} - ${book[2]}")
    
    while True:
        try:
            book_id = int(input("\nEnter the book ID you want to purchase: "))
            selected_book = get_book_by_id(book_id)
            if selected_book:
                break
            print("Invalid ID. Please choose a number from the list.")
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\nSelected: {selected_book[1]} by {selected_book[2]}")
    user_name = input("Enter your full name: ").strip()
    user_email = input("Enter your email address: ").strip()
    
    while True:
        try:
            quantity = int(input("Enter quantity: "))
            if quantity > 0:
                break
            print("Quantity must be at least 1.")
        except ValueError:
            print("Please enter a valid number.")
    
    total = selected_book[3] * quantity
    
    order = {
        'order_id': generate_order_id(),
        'user_name': user_name,
        'user_email': user_email,
        'book_id': selected_book[0],
        'book_title': selected_book[1],
        'book_author': selected_book[2],
        'quantity': quantity,
        'unit_price': selected_book[3],
        'total_price': round(total, 2),
        'order_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'pending'
    }
    
    save_order(order)
    
    ebook_file = generate_ebook_placeholder(order)
    print(f"\n[eBook placeholder generated: {ebook_file}]")
    
    send_order_email(order, ebook_file)
    
    print("\n" + "=" * 50)
    print("Order Confirmed!")
    print("=" * 50)
    print(f"Order ID: {order['order_id']}")
    print(f"Book: {order['book_title']}")
    print(f"Quantity: {order['quantity']}")
    print(f"Total: ${order['total_price']}")
    print(f"Order Date: {order['order_date']}")
    print(f"\nThank you, {order['user_name']}!")
    print(f"A confirmation email has been sent to: {order['user_email']}")
    print("=" * 50)

def main():
    create_order()

if __name__ == "__main__":
    main()