"""
Configuration module for Payment API
"""
import os

class Config:
    """Base configuration"""
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8100))
    DEBUG = os.getenv('DEBUG', True)
    DB_NAME = os.getenv('DB_NAME', 'payment.db')
    CORS_ORIGINS = ["*"]

config = Config()
