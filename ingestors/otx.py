"""
AlienVault OTX Ingestor - Fetches threat intelligence from OTX
"""
import requests
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.mongo import db_manager
from dotenv import load_dotenv

load_dotenv()

def fetch_otx_iocs():
    """Fetch IOCs from AlienVault OTX"""
    api_key = os.getenv('OTX_API_KEY')
    
    if not api_key:
        print("⚠️  OTX API key not found in .env file - skipping OTX")
        return []
    
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {
        'X-OTX-API-KEY': api_key
    }
    params = {
        'limit': 10,
        'page': 1
    }
    
    try:
        print("🔄 Fetching IOCs from AlienVault OTX...")
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            iocs = []
            
            for pulse in data.get('results', []):
                pulse_name = pulse.get('name', 'Unknown')
                
                for indicator in pulse.get('indicators', []):
                    ioc = {
                        'value': indicator.get('indicator'),
                        'type': indicator.get('type', 'unknown').lower(),
                        'source': 'AlienVault OTX',
                        'pulse': pulse_name,
                        'tags': pulse.get('tags', []),
                        'timestamp': datetime.utcnow()
                    }
                    iocs.append(ioc)
            
            return iocs
        elif response.status_code == 403:
            print("❌ OTX API error: Invalid API key")
            return []
        else:
            print(f"❌ OTX API error: Status {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching OTX IOCs: {e}")
        return []

def main():
    """Main execution"""
    if not db_manager.connect():
        print("❌ Failed to connect to database")
        return
    
    iocs = fetch_otx_iocs()
    
    if iocs:
        inserted = db_manager.insert_many_iocs(iocs)
        print(f"✅ OTX: Inserted {inserted} new IOCs (out of {len(iocs)} fetched)")
    else:
        print("⚠️  No IOCs fetched from OTX (API key may be missing)")

if __name__ == "__main__":
    main()
