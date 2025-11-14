"""
Statistics API routes
"""
from flask import Blueprint, jsonify
from utils.db_helper import query_db

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')

@stats_bp.route('/', methods=['GET'])
def get_stats():
    """Get system statistics"""
    
    # Total users
    total_users = query_db(
        'SELECT COUNT(*) as count FROM users',
        one=True
    )['count']
    
    # Total products
    total_products = query_db(
        'SELECT COUNT(*) as count FROM products',
        one=True
    )['count']
    
    # Total orders
    total_orders = query_db(
        'SELECT COUNT(*) as count FROM orders',
        one=True
    )['count']
    
    # Total revenue
    revenue_result = query_db(
        'SELECT SUM(total_amount) as total FROM orders WHERE status != "cancelled"',
        one=True
    )
    total_revenue = revenue_result['total'] or 0
    
    # Low stock products
    low_stock_count = query_db(
        'SELECT COUNT(*) as count FROM inventory WHERE stock < 20',
        one=True
    )['count']
    
    return jsonify({
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "low_stock_products": low_stock_count
    })

@stats_bp.route('/revenue', methods=['GET'])
def get_revenue_stats():
    """Get revenue statistics by status"""
    revenue_by_status = query_db('''
        SELECT 
            status,
            COUNT(*) as order_count,
            SUM(total_amount) as total_revenue
        FROM orders
        GROUP BY status
    ''')
    return jsonify(revenue_by_status)

@stats_bp.route('/products', methods=['GET'])
def get_product_stats():
    """Get product statistics by category"""
    product_stats = query_db('''
        SELECT 
            category,
            COUNT(*) as product_count,
            AVG(price) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price
        FROM products
        GROUP BY category
    ''')
    return jsonify(product_stats)

@stats_bp.route('/inventory', methods=['GET'])
def get_inventory_stats():
    """Get inventory statistics"""
    inventory_stats = query_db('''
        SELECT 
            SUM(stock) as total_stock,
            SUM(reserved) as total_reserved,
            SUM(stock - reserved) as total_available,
            COUNT(*) as product_count
        FROM inventory
    ''', one=True)
    return jsonify(inventory_stats)