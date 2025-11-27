"""
Register all route blueprints
"""
from flask import Blueprint

def register_routes(app):
    """Register all route blueprints with the app"""
    from .users import users_bp
    from .products import products_bp
    from .inventory import inventory_bp
    from .orders import orders_bp
    from .stats import stats_bp
    
    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(stats_bp)