"""
Inventory-related API routes
"""
from flask import Blueprint, request, jsonify
from utils.db_helper import query_db
from utils.response_helper import (
    success_response,
    not_found_response
)

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    """
    Get all inventory or filter by threshold
    ---
    parameters:
      - name: threshold
        in: query
        type: integer
        required: false
        description: Show only products with stock below this threshold
    responses:
      200:
        description: List of inventory items
        schema:
          type: array
          items:
            type: object
            properties:
              product_id:
                type: string
              name:
                type: string
              price:
                type: number
              stock:
                type: integer
              reserved:
                type: integer
              available:
                type: integer
    """
    threshold = request.args.get('threshold', type=int)

    if threshold is not None:
        # Get products with stock below threshold
        inventories = query_db('''
            SELECT i.*, p.name, p.price
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
            WHERE i.stock < ?
            ORDER BY i.stock ASC
        ''', (threshold,))
    else:
        # Get all inventory
        inventories = query_db('''
            SELECT i.*, p.name, p.price
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
            LIMIT 100
        ''')

    for inv in inventories:
        inv['available'] = inv['stock'] - inv['reserved']

    return success_response(inventories)

@inventory_bp.route('/low-stock', methods=['GET'])
def get_low_stock():
    """
    Get all products with low stock (< threshold)
    ---
    parameters:
      - name: threshold
        in: query
        type: integer
        required: false
        default: 20
        description: Stock threshold (default 20)
    responses:
      200:
        description: List of low stock inventory items
        schema:
          type: array
          items:
            type: object
            properties:
              product_id:
                type: string
              name:
                type: string
              price:
                type: number
              stock:
                type: integer
              reserved:
                type: integer
              available:
                type: integer
    """
    threshold = request.args.get('threshold', 20, type=int)

    inventories = query_db('''
        SELECT i.*, p.name, p.price
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        WHERE i.stock < ?
        ORDER BY i.stock ASC
    ''', (threshold,))

    for inv in inventories:
        inv['available'] = inv['stock'] - inv['reserved']

    return success_response(inventories)

@inventory_bp.route('/<product_id>', methods=['GET'])
def get_product_inventory(product_id):
    """
    Get inventory for a specific product by ID
    ---
    parameters:
      - name: product_id
        in: path
        type: string
        required: true
        description: The product ID
    responses:
      200:
        description: Product inventory details
        schema:
          type: object
          properties:
            product_id:
              type: string
            name:
              type: string
            price:
              type: number
            stock:
              type: integer
            reserved:
              type: integer
            available:
              type: integer
      404:
        description: Inventory not found
    """
    inventory = query_db('''
        SELECT i.*, p.name, p.price
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        WHERE i.product_id = ?
    ''', (product_id,), one=True)

    if inventory:
        inventory['available'] = inventory['stock'] - inventory['reserved']
        return success_response(inventory)
    return not_found_response("Inventory")