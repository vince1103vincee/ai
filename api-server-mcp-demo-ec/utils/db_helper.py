"""
Database helper functions
"""
from flask import g
import sqlite3
from config import config

def get_db():
    """
    Get database connection
    Creates a new connection if it doesn't exist in the Flask g object
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            config.DB_NAME,
            timeout=config.DB_TIMEOUT,
            check_same_thread=config.DB_CHECK_SAME_THREAD
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(error=None):
    """
    Close database connection
    Called automatically at the end of each request
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    """
    Execute a query and return results
    
    Args:
        query: SQL query string
        args: Query parameters
        one: Return single result if True, list otherwise
    
    Returns:
        Single row dict if one=True, list of dicts otherwise
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, args)
    
    if one:
        result = cursor.fetchone()
        return dict(result) if result else None
    else:
        results = cursor.fetchall()
        return [dict(row) for row in results]

def execute_db(query, args=()):
    """
    Execute a write query (INSERT, UPDATE, DELETE)
    
    Args:
        query: SQL query string
        args: Query parameters
    
    Returns:
        Number of affected rows
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, args)
    db.commit()
    return cursor.rowcount