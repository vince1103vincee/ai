"""
Main Flask application
"""
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

from config import config
from utils.db_helper import close_db
from routes import register_routes

def create_app(config_object=config):
    """
    Application factory pattern
    Creates and configures the Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Initialize CORS
    CORS(app, resources={r"/*": {"origins": config_object.CORS_ORIGINS}})
    
    # Register database teardown
    app.teardown_appcontext(close_db)
    
    # Register all routes
    register_routes(app)
    
    # Register root route
    @app.route('/', methods=['GET'])
    def index():
        """API index page"""
        return jsonify({
            "message": "Product Management API Server",
            "version": "2.0",
            "endpoints": {
                "users": "/users",
                "products": "/products",
                "inventory": "/inventory",
                "orders": "/orders",
                "stats": "/stats",
                "health": "/health"
            }
        })
    
    # Register health check
    @app.route('/health', methods=['GET'])
    def health_check():
        """API health check"""
        return jsonify({
            "status": "healthy",
            "service": "API Server",
            "timestamp": datetime.now().isoformat()
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("=" * 60)
    print("API Server Starting...")
    print("=" * 60)
    print(f"Address: http://{config.HOST}:{config.PORT}")
    print(f"Database: {config.DB_NAME}")
    print(f"Debug Mode: {config.DEBUG}")
    print("=" * 60)
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )