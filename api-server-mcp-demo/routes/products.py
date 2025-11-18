"""
Product-related API routes
"""
from flask import Blueprint, request
from utils.db_helper import query_db
from utils.response_helper import (
    success_response,
    not_found_response,
    no_results_response
)

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/', methods=['GET'])
def get_products():
    """
    Get all products or search by criteria
    Query params: name, category, brand
    """
    name = request.args.get('name')
    category = request.args.get('category')
    brand = request.args.get('brand')

    if name:
        products = query_db(
            'SELECT * FROM products WHERE LOWER(name) LIKE LOWER(?)',
            (f'%{name}%',)
        )
        if not products:
            return no_results_response("products")
        return success_response(products)

    elif category:
        products = query_db(
            'SELECT * FROM products WHERE LOWER(category) = LOWER(?)',
            (category,)
        )
        return success_response(products)

    elif brand:
        products = query_db(
            'SELECT * FROM products WHERE LOWER(brand) = LOWER(?)',
            (brand,)
        )
        return success_response(products)

    else:
        products = query_db('SELECT * FROM products LIMIT 100')
        return success_response(products)

@products_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get product by ID"""
    product = query_db(
        'SELECT * FROM products WHERE product_id = ?',
        (product_id,),
        one=True
    )
    if product:
        return success_response(product)
    return not_found_response("Product")

