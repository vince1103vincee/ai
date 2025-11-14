import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name='shop.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                created_at TEXT
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category TEXT,
                brand TEXT,
                created_at TEXT
            )
        ''')
        
        # Inventory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                product_id TEXT PRIMARY KEY,
                stock INTEGER NOT NULL,
                reserved INTEGER DEFAULT 0,
                last_updated TEXT,
                FOREIGN KEY (product_id) REFERENCES products (product_id)
            )
        ''')
        
        # Orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Order items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                product_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (order_id),
                FOREIGN KEY (product_id) REFERENCES products (product_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        self.insert_sample_data()
    
    def insert_sample_data(self):
        """Insert sample data for testing"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute('SELECT COUNT(*) as count FROM users')
        if cursor.fetchone()['count'] > 0:
            conn.close()
            return
        
        print("Inserting sample data...")
        
        # Insert users
        users = [
            ('u001', 'John Smith', 'john@example.com', '0912-345-678', 'Taipei City, Xinyi District', datetime.now().isoformat()),
            ('u002', 'Alice Chen', 'alice@example.com', '0923-456-789', 'New Taipei City, Banqiao District', datetime.now().isoformat()),
            ('u003', 'Bob Wang', 'bob@example.com', '0934-567-890', 'Taichung City, Xitun District', datetime.now().isoformat()),
            ('u004', 'Emma Lin', 'emma@example.com', '0945-678-901', 'Kaohsiung City, Qianzhen District', datetime.now().isoformat()),
        ]
        cursor.executemany('''
            INSERT INTO users (user_id, name, email, phone, address, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', users)
        
        # Insert products
        products = [
            ('p001', 'iPhone 15 Pro', 'Latest iPhone with A17 Pro chip', 36900, 'Phone', 'Apple', datetime.now().isoformat()),
            ('p002', 'AirPods Pro 2', 'Active noise cancellation wireless earbuds', 7990, 'Earbuds', 'Apple', datetime.now().isoformat()),
            ('p003', 'MacBook Air M3', '13-inch laptop', 37900, 'Laptop', 'Apple', datetime.now().isoformat()),
            ('p004', 'iPad Air', '10.9-inch tablet', 19900, 'Tablet', 'Apple', datetime.now().isoformat()),
            ('p005', 'Apple Watch Series 9', 'Smart watch', 12900, 'Watch', 'Apple', datetime.now().isoformat()),
            ('p006', 'Samsung Galaxy S24', 'Flagship phone', 27900, 'Phone', 'Samsung', datetime.now().isoformat()),
            ('p007', 'Sony WH-1000XM5', 'Premium noise canceling headphones', 10900, 'Headphones', 'Sony', datetime.now().isoformat()),
            ('p008', 'Dell XPS 13', '13-inch laptop', 42900, 'Laptop', 'Dell', datetime.now().isoformat()),
        ]
        cursor.executemany('''
            INSERT INTO products (product_id, name, description, price, category, brand, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', products)
        
        # Insert inventory
        inventory = [
            ('p001', 50, 5, datetime.now().isoformat()),
            ('p002', 120, 10, datetime.now().isoformat()),
            ('p003', 30, 3, datetime.now().isoformat()),
            ('p004', 80, 8, datetime.now().isoformat()),
            ('p005', 60, 6, datetime.now().isoformat()),
            ('p006', 40, 4, datetime.now().isoformat()),
            ('p007', 25, 2, datetime.now().isoformat()),
            ('p008', 15, 1, datetime.now().isoformat()),
        ]
        cursor.executemany('''
            INSERT INTO inventory (product_id, stock, reserved, last_updated)
            VALUES (?, ?, ?, ?)
        ''', inventory)
        
        # Insert orders
        base_date = datetime.now()
        orders = [
            ('o001', 'u001', 44890, 'completed', (base_date - timedelta(days=30)).isoformat()),
            ('o002', 'u001', 7990, 'completed', (base_date - timedelta(days=15)).isoformat()),
            ('o003', 'u002', 37900, 'shipped', (base_date - timedelta(days=5)).isoformat()),
            ('o004', 'u002', 32890, 'processing', (base_date - timedelta(days=2)).isoformat()),
            ('o005', 'u003', 27900, 'completed', (base_date - timedelta(days=20)).isoformat()),
            ('o006', 'u004', 10900, 'cancelled', (base_date - timedelta(days=10)).isoformat()),
        ]
        cursor.executemany('''
            INSERT INTO orders (order_id, user_id, total_amount, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', orders)
        
        # Insert order items
        order_items = [
            ('o001', 'p001', 1, 36900),
            ('o001', 'p002', 1, 7990),
            ('o002', 'p002', 1, 7990),
            ('o003', 'p003', 1, 37900),
            ('o004', 'p004', 1, 19900),
            ('o004', 'p005', 1, 12990),
            ('o005', 'p006', 1, 27900),
            ('o006', 'p007', 1, 10900),
        ]
        cursor.executemany('''
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (?, ?, ?, ?)
        ''', order_items)
        
        conn.commit()
        conn.close()
        print("Sample data inserted successfully!")

if __name__ == '__main__':
    db = Database()
    print("Database initialization completed!")