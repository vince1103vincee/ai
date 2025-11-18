"""
Order-related API routes
"""
from flask import Blueprint, request, jsonify
from utils.db_helper import query_db
from utils.response_helper import (
    success_response,
    error_response,
    not_found_response,
    no_results_response
)

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/', methods=['GET'])
def get_orders():
    """
    Get all orders or filter by criteria
    Query params: user_id, user_name, status, date_range
    """
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    status = request.args.get('status')
    date_range = request.args.get('date_range')

    if user_id or user_name:
        return get_user_orders(user_id, user_name, status, date_range)

    elif status:
        return get_orders_by_status(status)

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
        return not_found_response("Order")

    items = query_db('''
        SELECT oi.*, p.name as product_name
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = ?
    ''', (order_id,))

    order['items'] = items
    return success_response(order)

def get_user_orders(user_id=None, user_name=None, status=None, date_range=None):
    """Helper function to get user's orders by ID or name"""

    # If user_name is provided, search for the user first
    if user_name and not user_id:
        users = query_db(
            'SELECT user_id FROM users WHERE LOWER(name) LIKE LOWER(?)',
            (f'%{user_name}%',)
        )
        if users and len(users) > 0:
            user_id = users[0]['user_id']
        else:
            return not_found_response(f"User '{user_name}'")

    if not user_id:
        return error_response("Either user_id or user_name must be provided", 400)

    query = '''
        SELECT o.*, u.name as user_name
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        WHERE o.user_id = ?
    '''
    params = [user_id]

    if status:
        query += ' AND LOWER(o.status) = LOWER(?)'
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
    return success_response(orders)

@orders_bp.route('/user/<user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    """Get all orders for a user by ID
    Query params: status, date_range
    """
    status = request.args.get('status')
    date_range = request.args.get('date_range')
    return get_user_orders(user_id=user_id, status=status, date_range=date_range)

@orders_bp.route('/status/<status>', methods=['GET'])
def get_orders_by_status(status):
    """Get all orders with a specific status"""
    orders = query_db('''
        SELECT o.*, u.name as user_name
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        WHERE LOWER(o.status) = LOWER(?)
        ORDER BY o.created_at DESC
    ''', (status,))
    return success_response(orders)