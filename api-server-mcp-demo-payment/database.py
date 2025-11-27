"""
Database module for Payment API
"""
import sqlite3
from config import config

def get_db():
    """Get database connection"""
    db = sqlite3.connect(config.DB_NAME)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize database with tables"""
    db = get_db()
    cursor = db.cursor()

    # Create payments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id TEXT NOT NULL,
            buyer TEXT NOT NULL,
            email TEXT NOT NULL,
            payment_id TEXT UNIQUE NOT NULL,
            order_id TEXT NOT NULL,
            price REAL NOT NULL,
            currency TEXT NOT NULL DEFAULT 'TWD',
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    db.commit()
    db.close()

def insert_sample_data():
    """Insert sample payment and shop data"""
    db = get_db()
    cursor = db.cursor()

    # Create stores table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            email TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Sample store data
    sample_stores = [
        ('S001', 'Demo E-Store', '123 Main St, City A', 'store_a@example.com', '02-1234-5678'),
        ('S002', 'Electronics Hub', '456 Oak Ave, City B', 'store_b@example.com', '02-9876-5432'),
        ('S003', 'Digital Market', '789 Pine Rd, City C', 'store_c@example.com', '02-5555-6666'),
    ]

    try:
        for store_id, name, address, email, phone_number in sample_stores:
            cursor.execute('''
                INSERT INTO stores (store_id, name, address, email, phone_number)
                VALUES (?, ?, ?, ?, ?)
            ''', (store_id, name, address, email, phone_number))
        db.commit()
    except sqlite3.IntegrityError:
        # Data already exists
        pass

    # Sample payment data
    sample_payments = [
        ('S001', 'John Smith', 'john@example.com', 'PAY001', 'o001', 44890.00, 'USD', 'completed'),
        ('S001', 'John Smith', 'john@example.com', 'PAY002', 'o002', 7990.00, 'USD', 'completed'),
        ('S001', 'Alice Chen', 'alice@example.com', 'PAY003', 'o003', 37900.00, 'USD', 'completed'),
        ('S001', 'Alice Chen', 'alice@example.com', 'PAY004', 'o004', 32890.00, 'USD', 'pending'),
        ('S001', 'Bob Wang', 'bob@example.com', 'PAY005', 'o005', 27900.00, 'USD', 'completed'),
        ('S001', 'Emma Lin', 'emma@example.com', 'PAY006', 'o006', 10900.00, 'USD', 'failed'),
        ('S003', 'Andrew Bryant', 'andrew@example.com', 'PAY007', 'o007', 500.00, 'EUR', 'failed'),
        ('S002', 'Yamata Suzuki', 'allen@example.com', 'PAY008', 'o008', 120.00, 'JPY', 'pending'),
    ]

    try:
        for store_id, buyer, email, payment_id, order_id, price, currency, status in sample_payments:
            cursor.execute('''
                INSERT INTO payments (store_id, buyer, email, payment_id, order_id, price, currency, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (store_id, buyer, email, payment_id, order_id, price, currency, status))
        db.commit()
    except sqlite3.IntegrityError:
        # Data already exists
        pass
    finally:
        db.close()
