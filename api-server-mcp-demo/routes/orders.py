"""
Order-related API routes
"""
from flask import Blueprint, request, jsonify
from utils.db_helper import query_db

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/', methods=['GET'])
def get_orders():
    """
    Get all orders or search by criteria
    Query params: order_id, user_id, status, date_range
    """
    order_id = request.args.get('order_id')
    user_id = request.args.get('user_id')
    status = request.args.get('status')
    date_range = request.args.get('date_range')
    
    if order_id:
        return get_order_details(order_id)
    
    elif user_id:
        return get_user_orders(user_id, status, date_range)
    
    else:
        orders = query_db('''
            SELECT o.*, u.name as user_name
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            ORDER BY o.created_at DESC
            LIMIT 100
        ''')
        return jsonify(orders)

@orders_bp.route('/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get order details by ID"""
    return get_order_details(order_id)

def get_order_details(order_id):
    """Helper function to get order with items"""
    order = query_db('''
        SELECT o.*, u.name as user_name, u.email as user_email
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        WHERE o.order_id = ?
    ''', (order_id,), one=True)
    
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    items = query_db('''
        SELECT oi.*, p.name as product_name
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = ?
    ''', (order_id,))
    
    order['items'] = items
    return jsonify(order)

def get_user_orders(user_id, status=None, date_range=None):
    """Helper function to get user's orders"""
    query = '''
        SELECT o.*, u.name as user_name
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        WHERE o.user_id = ?
    '''
    params = [user_id]
    
    if status:
        query += ' AND o.status = ?'
        params.append(status)
    
    if date_range:
        if date_range == 'last_week':
            query += ' AND o.created_at >= datetime("now", "-7 days")'
        elif date_range == 'last_month':
            query += ' AND o.created_at >= datetime("now", "-30 days")'
        elif date_range == 'last_year':
            query += ' AND o.created_at >= datetime("now", "-365 days")'
    
    query += ' ORDER BY o.created_at DESC'
    
    orders = query_db(query, params)
    return jsonify(orders)

@orders_bp.route('/user/<user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    """Get all orders for a user"""
    status = request.args.get('status')
    date_range = request.args.get('date_range')
    return get_user_orders(user_id, status, date_range)

@orders_bp.route('/status/<status>', methods=['GET'])
def get_orders_by_status(status):
    """Get all orders with a specific status"""
    orders = query_db('''
        SELECT o.*, u.name as user_name
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        WHERE o.status = ?
        ORDER BY o.created_at DESC
    ''', (status,))
    return jsonify(orders)