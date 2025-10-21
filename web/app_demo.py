"""
Flask Demo Application for CTI Dashboard (No MongoDB Required)
Uses JSON file for data storage
"""
from flask import Flask, render_template, jsonify, request
import json
import os
from collections import Counter

app = Flask(__name__)

# Path to demo data
DEMO_DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'demo_data.json')

def load_demo_data():
    """Load data from JSON file"""
    if os.path.exists(DEMO_DATA_FILE):
        with open(DEMO_DATA_FILE, 'r') as f:
            return json.load(f)
    return []

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Get IOC statistics"""
    try:
        iocs = load_demo_data()
        
        # Count by type
        types = Counter(ioc.get('type', 'unknown') for ioc in iocs)
        by_type = [{'_id': k, 'count': v} for k, v in types.items()]
        by_type.sort(key=lambda x: x['count'], reverse=True)
        
        # Count by source
        sources = Counter(ioc.get('source', 'Unknown') for ioc in iocs)
        by_source = [{'_id': k, 'count': v} for k, v in sources.items()]
        by_source.sort(key=lambda x: x['count'], reverse=True)
        
        return jsonify({
            'total': len(iocs),
            'by_type': by_type,
            'by_source': by_source
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/iocs')
def get_iocs():
    """Get latest IOCs"""
    try:
        limit = request.args.get('limit', 100, type=int)
        iocs = load_demo_data()
        
        # Sort by timestamp (most recent first)
        iocs.sort(key=lambda x: x.get('timestamp', {}).get('$date', ''), reverse=True)
        
        return jsonify(iocs[:limit])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search')
def search_iocs():
    """Search IOCs by value"""
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        iocs = load_demo_data()
        results = [ioc for ioc in iocs if query in ioc.get('value', '').lower()]
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'database': 'demo_mode',
        'data_file': 'demo_data.json',
        'records': len(load_demo_data())
    })

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("="*70)
    print("🚀 Starting CTI Dashboard DEMO MODE (No MongoDB Required)")
    print("="*70)
    print()
    
    if not os.path.exists(DEMO_DATA_FILE):
        print("⚠️  Demo data file not found!")
        print("📊 Creating demo data...")
        import subprocess
        subprocess.run(['python', 'add_demo_data_simple.py'])
        print()
    
    data_count = len(load_demo_data())
    print(f"✅ Loaded {data_count} demo threats")
    print()
    print("🌐 Dashboard URL: http://127.0.0.1:5000")
    print("🔍 Search API: http://127.0.0.1:5000/api/search?q=<query>")
    print("📊 Stats API: http://127.0.0.1:5000/api/stats")
    print()
    print("="*70)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
