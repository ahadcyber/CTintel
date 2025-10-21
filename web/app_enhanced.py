"""
Enhanced Flask Web Application for CTI Dashboard
Production-ready with advanced features
"""
from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flasgger import Swagger
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import json
import csv
import io

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.mongo import db_manager
from bson import json_util
from config import get_config

# Initialize Flask app
app = Flask(__name__)
config = get_config()
app.config.from_object(config)

# Enable CORS
if config.ENABLE_CORS:
    CORS(app)

# Rate Limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[config.RATELIMIT_DEFAULT] if config.RATELIMIT_ENABLED else []
)

# Caching
cache = Cache(app)

# API Documentation
if config.ENABLE_API_DOCS:
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs"
    }
    swagger_template = {
        "info": {
            "title": "CTI Dashboard API",
            "description": "Cyber Threat Intelligence Dashboard API Documentation",
            "version": config.VERSION
        }
    }
    swagger = Swagger(app, config=swagger_config, template=swagger_template)

# Setup Logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
    handlers=[
        RotatingFileHandler(config.LOG_FILE, maxBytes=10485760, backupCount=5),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Connect to database on startup
if not db_manager.connect():
    logger.warning("MongoDB connection failed, retrying...")
    import time
    time.sleep(2)
    db_manager.connect()

def parse_json(data):
    """Helper to convert MongoDB documents to JSON"""
    return json.loads(json_util.dumps(data))


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/stats')
@cache.cached(timeout=60)
@limiter.limit("60 per minute")
def get_stats():
    """
    Get IOC statistics
    ---
    tags:
      - Statistics
    responses:
      200:
        description: IOC statistics
        schema:
          properties:
            total:
              type: integer
            by_type:
              type: array
            by_source:
              type: array
    """
    try:
        if db_manager.collection is None:
            db_manager.connect()
        
        stats = db_manager.get_stats()
        logger.info(f"Stats retrieved - Total: {stats.get('total', 0)}")
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error in get_stats: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/iocs')
@limiter.limit("100 per minute")
def get_iocs():
    """
    Get latest IOCs with pagination
    ---
    tags:
      - IOCs
    parameters:
      - name: limit
        in: query
        type: integer
        default: 100
        description: Number of IOCs to return
      - name: skip
        in: query
        type: integer
        default: 0
        description: Number of IOCs to skip
      - name: type
        in: query
        type: string
        description: Filter by IOC type
      - name: source
        in: query
        type: string
        description: Filter by source
    responses:
      200:
        description: List of IOCs
    """
    try:
        limit = min(request.args.get('limit', config.DEFAULT_PAGE_SIZE, type=int), config.MAX_PAGE_SIZE)
        skip = request.args.get('skip', 0, type=int)
        ioc_type = request.args.get('type', None)
        source = request.args.get('source', None)
        
        # Build filter
        filter_query = {}
        if ioc_type:
            filter_query['type'] = ioc_type
        if source:
            filter_query['source'] = source
        
        # Get IOCs
        iocs = list(db_manager.collection.find(filter_query)
                   .sort('timestamp', -1)
                   .skip(skip)
                   .limit(limit))
        
        total = db_manager.collection.count_documents(filter_query)
        
        logger.info(f"Retrieved {len(iocs)} IOCs (filter: {filter_query})")
        
        return jsonify({
            'iocs': parse_json(iocs),
            'total': total,
            'limit': limit,
            'skip': skip
        })
    except Exception as e:
        logger.error(f"Error in get_iocs: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/search')
@limiter.limit("30 per minute")
def search_iocs():
    """
    Search IOCs by value
    ---
    tags:
      - Search
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: Search query
      - name: limit
        in: query
        type: integer
        default: 50
        description: Maximum results
    responses:
      200:
        description: Search results
      400:
        description: Missing query parameter
    """
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        limit = min(request.args.get('limit', 50, type=int), 100)
        results = db_manager.search_iocs(query)[:limit]
        
        logger.info(f"Search query: '{query}' - Found {len(results)} results")
        return jsonify(parse_json(results))
    except Exception as e:
        logger.error(f"Error in search_iocs: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/<format>')
@limiter.limit("5 per hour")
def export_iocs(format):
    """
    Export IOCs in various formats
    ---
    tags:
      - Export
    parameters:
      - name: format
        in: path
        type: string
        required: true
        enum: [csv, json]
        description: Export format
      - name: type
        in: query
        type: string
        description: Filter by IOC type
      - name: source
        in: query
        type: string
        description: Filter by source
      - name: limit
        in: query
        type: integer
        default: 1000
        description: Maximum records
    responses:
      200:
        description: Exported file
      400:
        description: Invalid format
    """
    if not config.ENABLE_EXPORT:
        return jsonify({'error': 'Export feature is disabled'}), 403
    
    try:
        # Build filter
        filter_query = {}
        if request.args.get('type'):
            filter_query['type'] = request.args.get('type')
        if request.args.get('source'):
            filter_query['source'] = request.args.get('source')
        
        # Get IOCs
        limit = min(request.args.get('limit', 1000, type=int), config.MAX_EXPORT_RECORDS)
        iocs = list(db_manager.collection.find(filter_query).limit(limit))
        
        if format == 'json':
            output = io.BytesIO()
            output.write(json.dumps(parse_json(iocs), indent=2).encode('utf-8'))
            output.seek(0)
            
            return send_file(
                output,
                mimetype='application/json',
                as_attachment=True,
                download_name=f'iocs_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            )
        
        elif format == 'csv':
            output = io.StringIO()
            if iocs:
                writer = csv.DictWriter(output, fieldnames=['value', 'type', 'source', 'timestamp'])
                writer.writeheader()
                for ioc in iocs:
                    writer.writerow({
                        'value': ioc.get('value', ''),
                        'type': ioc.get('type', ''),
                        'source': ioc.get('source', ''),
                        'timestamp': ioc.get('timestamp', '')
                    })
            
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'iocs_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            )
        
        else:
            return jsonify({'error': 'Invalid format. Use csv or json'}), 400
        
        logger.info(f"Export completed: {format} - {len(iocs)} records")
    
    except Exception as e:
        logger.error(f"Error in export_iocs: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/sources')
@cache.cached(timeout=300)
def get_sources():
    """
    Get list of all IOC sources
    ---
    tags:
      - Metadata
    responses:
      200:
        description: List of sources
    """
    try:
        sources = db_manager.collection.distinct('source')
        return jsonify({'sources': sources})
    except Exception as e:
        logger.error(f"Error in get_sources: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/types')
@cache.cached(timeout=300)
def get_types():
    """
    Get list of all IOC types
    ---
    tags:
      - Metadata
    responses:
      200:
        description: List of IOC types
    """
    try:
        types = db_manager.collection.distinct('type')
        return jsonify({'types': types})
    except Exception as e:
        logger.error(f"Error in get_types: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/health')
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: Service health status
    """
    try:
        # Check database connection
        db_status = 'connected'
        if db_manager.client:
            db_manager.client.admin.command('ping')
        else:
            db_status = 'disconnected'
        
        return jsonify({
            'status': 'healthy',
            'version': config.VERSION,
            'database': db_status,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503


@app.route('/api/config')
def get_config_info():
    """
    Get public configuration information
    ---
    tags:
      - Configuration
    responses:
      200:
        description: Public configuration
    """
    return jsonify({
        'app_name': config.APP_NAME,
        'version': config.VERSION,
        'environment': config.FLASK_ENV,
        'features': {
            'export': config.ENABLE_EXPORT,
            'api_docs': config.ENABLE_API_DOCS,
            'rate_limiting': config.RATELIMIT_ENABLED
        },
        'pagination': {
            'default_page_size': config.DEFAULT_PAGE_SIZE,
            'max_page_size': config.MAX_PAGE_SIZE
        }
    })


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(429)
def ratelimit_handler(error):
    """Rate limit error handler"""
    return jsonify({'error': 'Rate limit exceeded', 'message': str(error)}), 429


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal server error: {error}", exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info(f"🚀 Starting {config.APP_NAME} v{config.VERSION}")
    logger.info(f"📊 Dashboard: http://{config.HOST}:{config.PORT}")
    logger.info(f"🔍 Environment: {config.FLASK_ENV}")
    
    if config.ENABLE_API_DOCS:
        logger.info(f"📚 API Docs: http://{config.HOST}:{config.PORT}/api/docs")
    
    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )
