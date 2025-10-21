"""
Spamhaus DROP Ingestor - Fetches malicious IP ranges
"""
import requests
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.mongo import db_manager

def fetch_spamhaus_iocs():
    """Fetch DROP list from Spamhaus"""
    url = "https://www.spamhaus.org/drop/drop.txt"
    
    try:
        print("🔄 Fetching IOCs from Spamhaus DROP...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            iocs = []
            lines = response.text.split('\n')
            
            for line in lines:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith(';'):
                    # DROP format: CIDR ; SBL reference
                    parts = line.split(';')
                    if parts:
                        ip_range = parts[0].strip()
                        reference = parts[1].strip() if len(parts) > 1 else 'N/A'
                        
                        ioc = {
                            'value': ip_range,
                            'type': 'ip_range',
                            'source': 'Spamhaus',
                            'reference': reference,
                            'timestamp': datetime.utcnow()
                        }
                        iocs.append(ioc)
            
            return iocs
        else:
            print(f"❌ Spamhaus API error: Status {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching Spamhaus IOCs: {e}")
        return []

def main():
    """Main execution"""
    if not db_manager.connect():
        print("❌ Failed to connect to database")
        return
    
    iocs = fetch_spamhaus_iocs()
    
    if iocs:
        inserted = db_manager.insert_many_iocs(iocs)
        print(f"✅ Spamhaus: Inserted {inserted} new IOCs (out of {len(iocs)} fetched)")
    else:
        print("⚠️  No IOCs fetched from Spamhaus")

if __name__ == "__main__":
    main()
