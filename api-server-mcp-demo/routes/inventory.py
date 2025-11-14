"""
Inventory-related API routes
"""
from flask import Blueprint, request, jsonify
from utils.db_helper import query_db

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    """
    Get inventory information
    Query params: product_id, low_stock
    """
    product_id = request.args.get('product_id')
    low_stock = request.args.get('low_stock', 'false').lower() == 'true'
    
    if product_id:
        inventory = query_db('''
            SELECT i.*, p.name, p.price
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
            WHERE i.product_id = ?
        ''', (product_id,), one=True)
        
        if inventory:
            inventory['available'] = inventory['stock'] - inventory['reserved']
            return jsonify(inventory)
        return jsonify({"error": "Inventory not found"}), 404
    
    elif low_stock:
        inventories = query_db('''
            SELECT i.*, p.name, p.price
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
            WHERE i.stock < 20
            ORDER BY i.stock ASC
        ''')
        
        for inv in inventories:
            inv['available'] = inv['stock'] - inv['reserved']
        
        return jsonify(inventories)
    
    else:
        inventories = query_db('''
            SELECT i.*, p.name, p.price
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
            LIMIT 100
        ''')
        
        for inv in inventories:
            inv['available'] = inv['stock'] - inv['reserved']
        
        return jsonify(inventories)

@inventory_bp.route('/<product_id>', methods=['GET'])
def get_product_inventory(product_id):
    """Get inventory for a specific product"""
    inventory = query_db('''
        SELECT i.*, p.name, p.price
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        WHERE i.product_id = ?
    ''', (product_id,), one=True)
    
    if inventory:
        inventory['available'] = inventory['stock'] - inventory['reserved']
        return jsonify(inventory)
    return jsonify({"error": "Inventory not found"}), 404

@inventory_bp.route('/low-stock', methods=['GET'])
def get_low_stock():
    """Get all products with low stock (< 20)"""
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
    
    return jsonify(inventories)