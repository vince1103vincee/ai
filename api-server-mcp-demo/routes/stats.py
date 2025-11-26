"""
Statistics API routes
"""
from flask import Blueprint, jsonify
from utils.db_helper import query_db
from utils.response_helper import success_response

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')

@stats_bp.route('/', methods=['GET'])
def get_stats():
    """
    Get overall system statistics
    ---
    responses:
      200:
        description: System statistics summary
        schema:
          type: object
          properties:
            total_users:
              type: integer
              description: Total number of users
            total_products:
              type: integer
              description: Total number of products
            total_orders:
              type: integer
              description: Total number of orders
            total_revenue:
              type: number
              description: Total revenue from completed orders
            low_stock_products:
              type: integer
              description: Number of products with stock below 20
    """
    
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

    return success_response({
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "low_stock_products": low_stock_count
    })

@stats_bp.route('/revenue', methods=['GET'])
def get_revenue_stats():
    """
    Get revenue statistics grouped by order status
    ---
    responses:
      200:
        description: Revenue statistics by status
        schema:
          type: array
          items:
            type: object
            properties:
              status:
                type: string
                description: Order status
              order_count:
                type: integer
                description: Number of orders with this status
              total_revenue:
                type: number
                description: Total revenue for this status
    """
    revenue_by_status = query_db('''
        SELECT
            status,
            COUNT(*) as order_count,
            SUM(total_amount) as total_revenue
        FROM orders
        GROUP BY status
    ''')
    return success_response(revenue_by_status)

@stats_bp.route('/products', methods=['GET'])
def get_product_stats():
    """
    Get product statistics grouped by category
    ---
    responses:
      200:
        description: Product statistics by category
        schema:
          type: array
          items:
            type: object
            properties:
              category:
                type: string
                description: Product category
              product_count:
                type: integer
                description: Number of products in this category
              avg_price:
                type: number
                description: Average price of products in this category
              min_price:
                type: number
                description: Minimum price of products in this category
              max_price:
                type: number
                description: Maximum price of products in this category
    """
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
    return success_response(product_stats)

@stats_bp.route('/inventory', methods=['GET'])
def get_inventory_stats():
    """
    Get inventory statistics overview
    ---
    responses:
      200:
        description: Inventory statistics summary
        schema:
          type: object
          properties:
            total_stock:
              type: integer
              description: Total items in stock across all products
            total_reserved:
              type: integer
              description: Total items reserved/on order
            total_available:
              type: integer
              description: Total items available for sale (stock - reserved)
            product_count:
              type: integer
              description: Number of products in inventory
    """
    inventory_stats = query_db('''
        SELECT
            SUM(stock) as total_stock,
            SUM(reserved) as total_reserved,
            SUM(stock - reserved) as total_available,
            COUNT(*) as product_count
        FROM inventory
    ''', one=True)
    return success_response(inventory_stats)