"""
ThreatFox Ingestor - Fetches malware IOCs from Abuse.ch
"""
import requests
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.mongo import db_manager

def fetch_threatfox_iocs():
    """Fetch IOCs from ThreatFox API"""
    url = "https://threatfox-api.abuse.ch/api/v1/"
    
    payload = {
        "query": "get_iocs",
        "days": 1
    }
    
    try:
        print("🔄 Fetching IOCs from ThreatFox...")
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('query_status') == 'ok':
                iocs = []
                raw_data = data.get('data', [])
                
                for item in raw_data:
                    ioc = {
                        'value': item.get('ioc'),
                        'type': item.get('ioc_type', 'unknown').lower(),
                        'source': 'ThreatFox',
                        'malware': item.get('malware_printable', 'N/A'),
                        'confidence': item.get('confidence_level', 0),
                        'timestamp': datetime.utcnow()
                    }
                    iocs.append(ioc)
                
                return iocs
            else:
                print(f"⚠️  ThreatFox query status: {data.get('query_status')}")
                return []
        else:
            print(f"❌ ThreatFox API error: Status {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching ThreatFox IOCs: {e}")
        return []

def main():
    """Main execution"""
    if not db_manager.connect():
        print("❌ Failed to connect to database")
        return
    
    iocs = fetch_threatfox_iocs()
    
    if iocs:
        inserted = db_manager.insert_many_iocs(iocs)
        print(f"✅ ThreatFox: Inserted {inserted} new IOCs (out of {len(iocs)} fetched)")
    else:
        print("⚠️  No IOCs fetched from ThreatFox")

if __name__ == "__main__":
    main()
