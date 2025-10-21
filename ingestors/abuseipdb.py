"""
AbuseIPDB Ingestor - Fetches malicious IP addresses
"""
import requests
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.mongo import db_manager
from dotenv import load_dotenv

load_dotenv()

def fetch_abuseipdb_iocs():
    """Fetch malicious IPs from AbuseIPDB"""
    api_key = os.getenv('ABUSEIPDB_KEY')
    
    if not api_key:
        print("⚠️  AbuseIPDB API key not found in .env file - skipping AbuseIPDB")
        return []
    
    url = "https://api.abuseipdb.com/api/v2/blacklist"
    headers = {
        'Key': api_key,
        'Accept': 'application/json'
    }
    params = {
        'confidenceMinimum': 90,
        'limit': 100
    }
    
    try:
        print("🔄 Fetching IOCs from AbuseIPDB...")
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            iocs = []
            
            for item in data.get('data', []):
                ioc = {
                    'value': item.get('ipAddress'),
                    'type': 'ip',
                    'source': 'AbuseIPDB',
                    'confidence': item.get('abuseConfidenceScore', 0),
                    'country': item.get('countryCode', 'Unknown'),
                    'timestamp': datetime.utcnow()
                }
                iocs.append(ioc)
            
            return iocs
        elif response.status_code == 401:
            print("❌ AbuseIPDB API error: Invalid API key")
            return []
        elif response.status_code == 429:
            print("⚠️  AbuseIPDB API rate limit exceeded")
            return []
        else:
            print(f"❌ AbuseIPDB API error: Status {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching AbuseIPDB IOCs: {e}")
        return []

def main():
    """Main execution"""
    if not db_manager.connect():
        print("❌ Failed to connect to database")
        return
    
    iocs = fetch_abuseipdb_iocs()
    
    if iocs:
        inserted = db_manager.insert_many_iocs(iocs)
        print(f"✅ AbuseIPDB: Inserted {inserted} new IOCs (out of {len(iocs)} fetched)")
    else:
        print("⚠️  No IOCs fetched from AbuseIPDB (API key may be missing)")

if __name__ == "__main__":
    main()
