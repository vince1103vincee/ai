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
    ---
    parameters:
      - name: user_id
        in: query
        type: string
        required: false
        description: Filter orders by user ID
      - name: user_name
        in: query
        type: string
        required: false
        description: Filter orders by user name (case-insensitive partial match)
      - name: status
        in: query
        type: string
        required: false
        description: Filter orders by status (pending, shipped, delivered, cancelled)
      - name: date_range
        in: query
        type: string
        enum: [last_week, last_month, last_year]
        required: false
        description: Filter orders by date range
    responses:
      200:
        description: List of orders
        schema:
          type: array
          items:
            type: object
            properties:
              order_id:
                type: string
              user_id:
                type: string
              user_name:
                type: string
              total_amount:
                type: number
              status:
                type: string
              created_at:
                type: string
      404:
        description: No orders found
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
    """
    Get order details by ID
    ---
    parameters:
      - name: order_id
        in: path
        type: string
        required: true
        description: The order ID
    responses:
      200:
        description: Order details with items
        schema:
          type: object
          properties:
            order_id:
              type: string
            user_id:
              type: string
            user_name:
              type: string
            user_email:
              type: string
            total_amount:
              type: number
            status:
              type: string
            created_at:
              type: string
            items:
              type: array
              items:
                type: object
                properties:
                  order_item_id:
                    type: string
                  product_id:
                    type: string
                  product_name:
                    type: string
                  quantity:
                    type: integer
      404:
        description: Order not found
    """
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
    """
    Get all orders for a user by ID
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: The user ID
      - name: status
        in: query
        type: string
        required: false
        description: Filter by order status
      - name: date_range
        in: query
        type: string
        enum: [last_week, last_month, last_year]
        required: false
        description: Filter by date range
    responses:
      200:
        description: List of user orders
        schema:
          type: array
          items:
            type: object
      400:
        description: Invalid parameters
      404:
        description: User not found
    """
    status = request.args.get('status')
    date_range = request.args.get('date_range')
    return get_user_orders(user_id=user_id, status=status, date_range=date_range)

@orders_bp.route('/status/<status>', methods=['GET'])
def get_orders_by_status(status):
    """
    Get all orders with a specific status
    ---
    parameters:
      - name: status
        in: path
        type: string
        required: true
        enum: [pending, shipped, delivered, cancelled]
        description: The order status
    responses:
      200:
        description: List of orders with specified status
        schema:
          type: array
          items:
            type: object
            properties:
              order_id:
                type: string
              user_id:
                type: string
              user_name:
                type: string
              total_amount:
                type: number
              status:
                type: string
      404:
        description: No orders found with this status
    """
    orders = query_db('''
        SELECT o.*, u.name as user_name
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        WHERE LOWER(o.status) = LOWER(?)
        ORDER BY o.created_at DESC
    ''', (status,))
    return success_response(orders)