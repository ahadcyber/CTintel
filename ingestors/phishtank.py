"""
PhishTank Ingestor - Fetches phishing URLs
"""
import requests
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.mongo import db_manager

def fetch_phishtank_iocs():
    """Fetch phishing URLs from PhishTank"""
    url = "https://data.phishtank.com/data/online-valid.json"
    
    try:
        print("🔄 Fetching IOCs from PhishTank...")
        response = requests.get(url, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            iocs = []
            
            # Limit to recent 500 entries to avoid overwhelming the database
            for item in data[:500]:
                ioc = {
                    'value': item.get('url'),
                    'type': 'url',
                    'source': 'PhishTank',
                    'verified': item.get('verified', False),
                    'target': item.get('target', 'Unknown'),
                    'timestamp': datetime.utcnow()
                }
                iocs.append(ioc)
            
            return iocs
        else:
            print(f"❌ PhishTank API error: Status {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching PhishTank IOCs: {e}")
        return []

def main():
    """Main execution"""
    if not db_manager.connect():
        print("❌ Failed to connect to database")
        return
    
    iocs = fetch_phishtank_iocs()
    
    if iocs:
        inserted = db_manager.insert_many_iocs(iocs)
        print(f"✅ PhishTank: Inserted {inserted} new IOCs (out of {len(iocs)} fetched)")
    else:
        print("⚠️  No IOCs fetched from PhishTank")

if __name__ == "__main__":
    main()
