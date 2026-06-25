import json
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Email configuration - REPLACE WITH YOUR OWN
EMAIL_SENDER = "rossjiao122@gmail.com"
EMAIL_PASSWORD = "gnhx ztuo cekb ocin"  # 16-digit app password
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587

def load_books():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'books.json')
    with open(file_path, 'r') as f:
        return json.load(f)

def load_orders():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'orders.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def save_order(order, orders):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'orders.json')
    orders.append(order)
    with open(file_path, 'w') as f:
        json.dump(orders, f, indent=2)

def generate_order_id():
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    orders = load_orders()
    today_orders = [o for o in orders if o['order_id'].startswith(f"ORD-{date_str}")]
    count = len(today_orders) + 1
    return f"ORD-{date_str}-{count:04d}"

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
    books = load_books()
    
    print("\n" + "=" * 50)
    print("Place an Order")
    print("=" * 50)
    
    print("\nAvailable Books:")
    for book in books:
        print(f"  {book['id']}. {book['title']} - ${book['price']}")
    
    while True:
        try:
            book_id = int(input("\nEnter the book ID you want to purchase: "))
            selected_book = next((b for b in books if b['id'] == book_id), None)
            if selected_book:
                break
            print("Invalid ID. Please choose a number from the list.")
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\nSelected: {selected_book['title']} by {selected_book['author']}")
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
    
    total = selected_book['price'] * quantity
    
    order = {
        'order_id': generate_order_id(),
        'user_name': user_name,
        'user_email': user_email,
        'book_id': selected_book['id'],
        'book_title': selected_book['title'],
        'book_author': selected_book['author'],
        'quantity': quantity,
        'unit_price': selected_book['price'],
        'total_price': round(total, 2),
        'order_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'pending'
    }
    
    orders = load_orders()
    save_order(order, orders)
    
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