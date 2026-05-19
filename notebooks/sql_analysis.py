import sqlite3
import pandas as pd
import numpy as np

# Create SQLite database
conn = sqlite3.connect('data/ecommerce.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    price REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
)
''')

# Insert sample data
customers_data = [
    (1, 'Alice Smith', 'USA'),
    (2, 'Bob Johnson', 'UK'),
    (3, 'Carlos Lopez', 'Spain'),
    (4, 'Diana Prince', 'Canada'),
    (5, 'Ethan Hunt', 'USA')
]
cursor.executemany('INSERT OR IGNORE INTO customers VALUES (?,?,?)', customers_data)

products_data = [
    (1, 'Laptop', 999.99),
    (2, 'Mouse', 29.99),
    (3, 'Keyboard', 79.99),
    (4, 'Monitor', 299.99),
    (5, 'USB Cable', 9.99)
]
cursor.executemany('INSERT OR IGNORE INTO products VALUES (?,?,?)', products_data)

orders_data = [
    (1, 1, '2024-01-15', 1029.98),
    (2, 2, '2024-01-20', 109.98),
    (3, 3, '2024-02-10', 1099.98),
    (4, 1, '2024-02-25', 79.99),
    (5, 4, '2024-03-05', 39.98),
    (6, 5, '2024-03-15', 999.99)
]
cursor.executemany('INSERT OR IGNORE INTO orders VALUES (?,?,?,?)', orders_data)

order_items_data = [
    (1, 1, 1, 1), (2, 1, 2, 1),
    (3, 2, 2, 1), (4, 2, 5, 2),
    (5, 3, 1, 1), (6, 3, 3, 1),
    (7, 4, 3, 1), (8, 5, 2, 1), (9, 5, 5, 2),
    (10, 6, 1, 1)
]
cursor.executemany('INSERT OR IGNORE INTO order_items VALUES (?,?,?,?)', order_items_data)

conn.commit()

# SQL Queries for KPIs
print("\n📊 E-COMMERCE ANALYSIS RESULTS\n")
print("1. Top 5 Products by Revenue:")
query1 = '''
SELECT p.product_name, SUM(oi.quantity * p.price) as revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 5
'''
print(pd.read_sql_query(query1, conn))

print("\n2. Monthly Sales Trend:")
query2 = '''
SELECT strftime('%Y-%m', order_date) as month,
       COUNT(order_id) as num_orders,
       SUM(total_amount) as total_sales
FROM orders
GROUP BY month
ORDER BY month
'''
print(pd.read_sql_query(query2, conn))

print("\n3. Customer Lifetime Value (Top 5):")
query3 = '''
SELECT c.name, COUNT(o.order_id) as num_orders, SUM(o.total_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 5
'''
print(pd.read_sql_query(query3, conn))

print("\n4. Repeat Customers:")
query4 = '''
SELECT COUNT(*) as repeat_customers
FROM (
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    HAVING COUNT(order_id) > 1
)
'''
print(pd.read_sql_query(query4, conn))

conn.close()
print("\n✅ Analysis complete! Database saved to 'data/ecommerce.db'")
