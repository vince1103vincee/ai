"""
Flask Payment API Server
Provides endpoints to manage and retrieve payment information
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from datetime import datetime
import os

from config import config
from database import init_db, insert_sample_data
from utils import close_db, get_all_payments, get_all_stores, get_payments_by_email, get_payments_by_store_id, get_store_by_id

def create_app(config_object=config):
    """
    Application factory pattern
    Creates and configures the Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize CORS
    CORS(app, resources={r"/*": {"origins": config_object.CORS_ORIGINS}})

    # Initialize Swagger/OpenAPI
    swagger = Swagger(app, template={
        "openapi": "3.1.0",
        "info": {
            "title": "Payment Management API",
            "version": "1.0",
            "description": "API Server for payment management system",
            "contact": {
                "name": "API Support",
                "email": "support@example.com"
            }
        },
        "servers": [
            {
                "url": "http://localhost:8100",
                "description": "Development server"
            }
        ]
    })

    # Register database teardown
    app.teardown_appcontext(close_db)

    # Register root route
    @app.route('/', methods=['GET'])
    def index():
        """API index page"""
        return jsonify({
            "message": "Payment Management API Server",
            "version": "1.0",
            "endpoints": {
                "payments": "/payment",
                "stores": "/store",
                "health": "/health"
            }
        })

    # Register health check
    @app.route('/health', methods=['GET'])
    def health_check():
        """API health check"""
        return jsonify({
            "status": "healthy",
            "service": "Payment API Server",
            "timestamp": datetime.now().isoformat()
        })

    # Payment endpoints
    @app.route('/payment', methods=['GET'])
    def get_payments():
        """
        Get all payments or search by email/store_id
        ---
        parameters:
          - name: email
            in: query
            type: string
            description: Filter payments by buyer email
          - name: store_id
            in: query
            type: string
            description: Filter payments by store_id
        responses:
          200:
            description: List of payments
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "success"
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      store_id:
                        type: string
                      buyer:
                        type: string
                      email:
                        type: string
                      payment_id:
                        type: string
                      order_id:
                        type: string
                      price:
                        type: number
                      currency:
                        type: string
                      status:
                        type: string
                      created_at:
                        type: string
        """
        try:
            email = request.args.get('email')
            store_id = request.args.get('store_id')

            if email:
                payments = get_payments_by_email(email)
            elif store_id:
                payments = get_payments_by_store_id(store_id)
            else:
                payments = get_all_payments()

            return jsonify({
                "status": "success",
                "data": payments,
                "count": len(payments)
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    # Store endpoints
    @app.route('/store', methods=['GET'])
    def get_stores():
        """
        Get all stores or search by store_id
        ---
        parameters:
          - name: store_id
            in: query
            type: string
            description: Filter stores by store_id
        responses:
          200:
            description: List of stores or single store
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "success"
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      store_id:
                        type: string
                      name:
                        type: string
                      address:
                        type: string
                      email:
                        type: string
                      phone_number:
                        type: string
                      created_at:
                        type: string
        """
        try:
            store_id = request.args.get('store_id')

            if store_id:
                store = get_store_by_id(store_id)
                if store:
                    return jsonify({
                        "status": "success",
                        "data": [store],
                        "count": 1
                    }), 200
                else:
                    return jsonify({
                        "status": "success",
                        "data": [],
                        "count": 0
                    }), 200
            else:
                stores = get_all_stores()
                return jsonify({
                    "status": "success",
                    "data": stores,
                    "count": len(stores)
                }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    return app

if __name__ == '__main__':
    # Initialize database
    init_db()
    insert_sample_data()

    app = create_app()

    print("=" * 60)
    print("Payment API Server Starting...")
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
