"""
Configuration Management for CTI Dashboard
Supports multiple environments: development, production, testing
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    
    # Application
    APP_NAME = "CTI Dashboard"
    VERSION = "2.0.0"
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = False
    TESTING = False
    
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'cti_dashboard')
    MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'iocs')
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # API Keys
    OTX_API_KEY = os.getenv('OTX_API_KEY', '')
    ABUSEIPDB_KEY = os.getenv('ABUSEIPDB_KEY', '')
    
    # Rate Limiting
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'true').lower() == 'true'
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '100 per hour')
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    
    # Caching
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'SimpleCache')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/cti_dashboard.log')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Security
    ENABLE_CORS = os.getenv('ENABLE_CORS', 'true').lower() == 'true'
    ENABLE_HTTPS = os.getenv('ENABLE_HTTPS', 'false').lower() == 'true'
    
    # Features
    ENABLE_EXPORT = os.getenv('ENABLE_EXPORT', 'true').lower() == 'true'
    ENABLE_API_DOCS = os.getenv('ENABLE_API_DOCS', 'true').lower() == 'true'
    MAX_EXPORT_RECORDS = int(os.getenv('MAX_EXPORT_RECORDS', 10000))
    
    # Pagination
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', 100))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', 1000))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'
    LOG_LEVEL = 'DEBUG'
    RATELIMIT_ENABLED = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    LOG_LEVEL = 'WARNING'
    RATELIMIT_ENABLED = True
    ENABLE_HTTPS = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    MONGO_DB_NAME = 'cti_dashboard_test'
    RATELIMIT_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'production')
    return config.get(env, config['default'])
