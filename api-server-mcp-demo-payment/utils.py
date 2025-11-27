"""
Utility functions for Payment API
"""
from database import get_db

def close_db(error=None):
    """Close database connection"""
    pass

def get_all_payments():
    """Retrieve all payments from database"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT id, store_id, buyer, email, payment_id, order_id, price, currency, status, created_at, updated_at
        FROM payments
        ORDER BY created_at DESC
    ''')
    payments = cursor.fetchall()
    db.close()

    return [dict(payment) for payment in payments]

def get_payment_by_id(payment_id):
    """Retrieve a single payment by payment_id"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT id, store_id, buyer, email, payment_id, order_id, price, currency, status, created_at, updated_at
        FROM payments
        WHERE payment_id = ?
    ''', (payment_id,))
    payment = cursor.fetchone()
    db.close()

    return dict(payment) if payment else None

def get_payments_by_email(email):
    """Retrieve all payments by email"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT id, store_id, buyer, email, payment_id, order_id, price, currency, status, created_at, updated_at
        FROM payments
        WHERE email = ?
        ORDER BY created_at DESC
    ''', (email,))
    payments = cursor.fetchall()
    db.close()

    return [dict(payment) for payment in payments]

def get_payments_by_store_id(store_id):
    """Retrieve all payments by store_id"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT id, store_id, buyer, email, payment_id, order_id, price, currency, status, created_at, updated_at
        FROM payments
        WHERE store_id = ?
        ORDER BY created_at DESC
    ''', (store_id,))
    payments = cursor.fetchall()
    db.close()

    return [dict(payment) for payment in payments]

def get_all_stores():
    """Retrieve all stores from database"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT id, store_id, name, address, email, phone_number, created_at, updated_at
        FROM stores
        ORDER BY created_at DESC
    ''')
    stores = cursor.fetchall()
    db.close()

    return [dict(store) for store in stores]

def get_store_by_id(store_id):
    """Retrieve a single store by store_id"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT id, store_id, name, address, email, phone_number, created_at, updated_at
        FROM stores
        WHERE store_id = ?
    ''', (store_id,))
    store = cursor.fetchone()
    db.close()

    return dict(store) if store else None
