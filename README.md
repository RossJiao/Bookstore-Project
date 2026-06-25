# Bookstore Project

## Overview
An e-commerce platform for books that allows users to search for books, place orders, and receive a confirmation email with an eBook placeholder file attached.

## Features
- **Search books** by title, author, or genre
- **Place orders** with user name and email
- **Generate unique order IDs** (e.g., `ORD-20260625-0001`)
- **Create eBook placeholder files** for each order
- **Send confirmation emails** with order details and attachment

## Repository Structure
├── search.py # Book search module
├── order.py # Order placement and email module
├── books.json # Book database (JSON format)
├── orders.json # Order records (JSON format)
├── orders/ # eBook placeholder files
│ └── ORD-*.txt
└── README.md # This file

## Setup

### Prerequisites
- Python 3.x
- Gmail account (for email sending)

### Clone the repository
```bash
git clone https://github.com/RossJiao/bookstore-project.git
cd bookstore-project
Configure email (optional)
If you want to use the email feature, update order.py with your email credentials:
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"


Usage Example
Search
text
$ python3 search.py

Search for a book (title/author/genre), or 'quit' to exit:
> fiction

ID: 1 - The Great Gatsby
ID: 2 - 1984
ID: 4 - The Catcher in the Rye
Order
text
$ python3 order.py

Available Books:
  1. The Great Gatsby - $12.99
  2. 1984 - $14.99

Enter the book ID: 1
Enter your full name: John Doe
Enter your email address: john@example.com
Enter quantity: 1

Order ID: ORD-20260625-0001
Total: $12.99
Thank you, John Doe!
A confirmation email has been sent to: john@example.com
Sample Email Received

Subject: Bookstore Order Confirmation - ORD-20260625-0001

Dear John Doe,

Thank you for your order at Ross' Bookstore!

Order Details:
----------------------------------------
Order ID: ORD-20260625-0001
Book: The Great Gatsby
Author: F. Scott Fitzgerald
Quantity: 1
Total: $12.99
Order Date: 2026-06-25 22:47:33
----------------------------------------

Your eBook placeholder is attached to this email.
Sample eBook Placeholder File
========================================
EBOOK PLACEHOLDER
========================================
Order ID: ORD-20260625-0001
Book: The Great Gatsby
Author: F. Scott Fitzgerald
User: John Doe
Email: john@example.com
Order Date: 2026-06-25 22:47:33
========================================
This is a placeholder file for your eBook.
The actual eBook will be available for download at:
https://bookstore.example.com/download/ORD-20260625-0001
========================================
Technology Stack
Python 3 (standard library only)

json, os, smtplib, email, datetime

Links
GitHub: https://github.com/RossJiao/bookstore-project

Author
Ross Dingyan Jiao
