"""
Flask Web Application for CTI Dashboard
"""
from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS
import sys
import os
import csv
import io
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.mongo import db_manager
from ingestors.virustotal import vt_checker
from bson import json_util
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to database on startup
if not db_manager.connect():
    print("⚠️  Warning: MongoDB connection failed, retrying...")
    import time
    time.sleep(2)
    db_manager.connect()

def parse_json(data):
    """Helper to convert MongoDB documents to JSON"""
    return json.loads(json_util.dumps(data))

@app.route('/')
def index():
    """Main dashboard page"""
    response = app.make_response(render_template('dashboard.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/stats')
def get_stats():
    """Get IOC statistics"""
    try:
        # Verify connection
        if db_manager.collection is None:
            print("ERROR: Database collection is None!")
            db_manager.connect()
        
        stats = db_manager.get_stats()
        print(f"DEBUG: Stats retrieved - Total: {stats.get('total', 0)}")
        return jsonify(stats)
    except Exception as e:
        print(f"ERROR in get_stats: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/iocs')
def get_iocs():
    """Get latest IOCs"""
    try:
        limit = request.args.get('limit', 100, type=int)
        iocs = db_manager.get_all_iocs(limit=limit)
        return jsonify(parse_json(iocs))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search')
def search_iocs():
    """Search IOCs by value"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        results = db_manager.search_iocs(query)
        return jsonify(parse_json(results))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'database': 'connected' if db_manager.client else 'disconnected'
    })

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/lookup', methods=['POST'])
def lookup_threat():
    """Lookup threat in VirusTotal and local database"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        lookup_type = data.get('type', 'auto')  # ip, domain, url, hash, or auto
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        # Check local database first
        local_results = db_manager.search_iocs(query)
        
        # Check VirusTotal
        vt_result = {}
        if lookup_type == 'ip' or (lookup_type == 'auto' and _is_ip(query)):
            vt_result = vt_checker.check_ip(query)
        elif lookup_type == 'domain' or (lookup_type == 'auto' and _is_domain(query)):
            vt_result = vt_checker.check_domain(query)
        elif lookup_type == 'url' or (lookup_type == 'auto' and _is_url(query)):
            vt_result = vt_checker.check_url(query)
        elif lookup_type == 'hash' or (lookup_type == 'auto' and _is_hash(query)):
            vt_result = vt_checker.check_hash(query)
        
        return jsonify({
            'query': query,
            'local_matches': parse_json(local_results),
            'virustotal': vt_result,
            'total_local_matches': len(local_results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export')
def export_iocs():
    """Export IOCs in CSV or JSON format"""
    try:
        format_type = request.args.get('format', 'json').lower()
        limit = request.args.get('limit', 1000, type=int)
        tag = request.args.get('tag', None)
        
        # Get IOCs
        if tag:
            iocs = db_manager.get_iocs_by_tag(tag)
        else:
            iocs = db_manager.get_all_iocs(limit=limit)
        
        if format_type == 'csv':
            # Generate CSV
            output = io.StringIO()
            if iocs:
                fieldnames = ['value', 'type', 'source', 'timestamp', 'tags']
                writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                
                for ioc in iocs:
                    # Convert ObjectId and datetime to string
                    ioc['_id'] = str(ioc.get('_id', ''))
                    ioc['timestamp'] = str(ioc.get('timestamp', ''))
                    ioc['tags'] = ','.join(ioc.get('tags', []))
                    writer.writerow(ioc)
            
            response = Response(output.getvalue(), mimetype='text/csv')
            response.headers['Content-Disposition'] = 'attachment; filename=iocs_export.csv'
            return response
        else:
            # Return JSON
            response = Response(json_util.dumps(iocs), mimetype='application/json')
            response.headers['Content-Disposition'] = 'attachment; filename=iocs_export.json'
            return response
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tags/<ioc_id>', methods=['POST', 'DELETE'])
def manage_tags(ioc_id):
    """Add or remove tags from an IOC"""
    try:
        data = request.get_json()
        tag = data.get('tag', '').strip()
        
        if not tag:
            return jsonify({'error': 'Tag parameter is required'}), 400
        
        if request.method == 'POST':
            success = db_manager.add_tag_to_ioc(ioc_id, tag)
            return jsonify({'success': success, 'message': 'Tag added' if success else 'Failed to add tag'})
        else:  # DELETE
            success = db_manager.remove_tag_from_ioc(ioc_id, tag)
            return jsonify({'success': success, 'message': 'Tag removed' if success else 'Failed to remove tag'})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trends')
def get_trends():
    """Get IOC trends over time"""
    try:
        days = request.args.get('days', 7, type=int)
        trends = db_manager.get_trends(days=days)
        return jsonify(trends)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/threat-levels')
def get_threat_levels():
    """Get statistics by threat level"""
    try:
        stats = db_manager.get_threat_level_stats()
        return jsonify(parse_json(stats))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _is_ip(value):
    """Check if value is an IP address"""
    import re
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    return bool(re.match(ip_pattern, value))

def _is_domain(value):
    """Check if value is a domain"""
    import re
    domain_pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(domain_pattern, value))

def _is_url(value):
    """Check if value is a URL"""
    return value.startswith(('http://', 'https://'))

def _is_hash(value):
    """Check if value is a file hash (MD5, SHA1, SHA256)"""
    import re
    hash_pattern = r'^[a-fA-F0-9]{32}$|^[a-fA-F0-9]{40}$|^[a-fA-F0-9]{64}$'
    return bool(re.match(hash_pattern, value))

if __name__ == '__main__':
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('FLASK_PORT', '5000'))
    print(f"🚀 Starting CTI Dashboard on http://127.0.0.1:{port}")
    print(f"📊 Dashboard: http://127.0.0.1:{port}")
    print(f"🔍 Search API: http://127.0.0.1:{port}/api/search?q=<query>")
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
