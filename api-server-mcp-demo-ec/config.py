"""
Application configuration
"""
import os

class Config:
    """Base configuration"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_NAME = os.path.join(BASE_DIR, 'shop.db')
    
    # Flask settings
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 8000
    
    # CORS settings
    CORS_ORIGINS = '*'
    
    # Database settings
    DB_TIMEOUT = 5
    DB_CHECK_SAME_THREAD = False

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Default configuration
config = DevelopmentConfig()