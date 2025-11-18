"""
Product-related API routes
"""
from flask import Blueprint, request, jsonify
from utils.db_helper import query_db

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/', methods=['GET'])
def get_products():
    """
    Get all products or search by criteria
    Query params: name, product_id, category, brand
    """
    name = request.args.get('name')
    product_id = request.args.get('product_id')
    category = request.args.get('category')
    brand = request.args.get('brand')
    
    if product_id:
        product = query_db(
            'SELECT * FROM products WHERE product_id = ?',
            (product_id,),
            one=True
        )
        if product:
            return jsonify(product)
        return jsonify({"error": "Product not found"}), 404
    
    elif name:
        products = query_db(
            'SELECT * FROM products WHERE LOWER(name) LIKE LOWER(?)',
            (f'%{name}%',)
        )
        if products:
            return jsonify(products)
        return jsonify({"error": "No products found"}), 404

    elif category:
        products = query_db(
            'SELECT * FROM products WHERE LOWER(category) = LOWER(?)',
            (category,)
        )
        return jsonify(products)

    elif brand:
        products = query_db(
            'SELECT * FROM products WHERE LOWER(brand) = LOWER(?)',
            (brand,)
        )
        return jsonify(products)
    
    else:
        products = query_db('SELECT * FROM products LIMIT 100')
        return jsonify(products)

@products_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get product by ID"""
    product = query_db(
        'SELECT * FROM products WHERE product_id = ?',
        (product_id,),
        one=True
    )
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

