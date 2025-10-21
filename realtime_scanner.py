"""
Real-time IOC Scanner - Automatically fetches fresh threat intelligence
Runs continuously in the background
"""
import time
import schedule
import logging
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestors import threatfox, phishtank, spamhaus, otx, abuseipdb
from db.mongo import db_manager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def fetch_all_iocs():
    """Fetch IOCs from all sources"""
    logger.info("="*70)
    logger.info("🔄 REAL-TIME IOC SCAN STARTED")
    logger.info("="*70)
    
    # Connect to database
    if not db_manager.client:
        db_manager.connect()
    
    total_new = 0
    
    # ThreatFox
    try:
        logger.info("📡 Fetching from ThreatFox...")
        result = threatfox.main()
        if result:
            total_new += result
        logger.info(f"✅ ThreatFox complete")
    except Exception as e:
        logger.error(f"❌ ThreatFox error: {e}")
    
    # PhishTank
    try:
        logger.info("📡 Fetching from PhishTank...")
        result = phishtank.main()
        if result:
            total_new += result
        logger.info(f"✅ PhishTank complete")
    except Exception as e:
        logger.error(f"❌ PhishTank error: {e}")
    
    # Spamhaus
    try:
        logger.info("📡 Fetching from Spamhaus...")
        result = spamhaus.main()
        if result:
            total_new += result
        logger.info(f"✅ Spamhaus complete")
    except Exception as e:
        logger.error(f"❌ Spamhaus error: {e}")
    
    # OTX
    try:
        logger.info("📡 Fetching from AlienVault OTX...")
        result = otx.main()
        if result:
            total_new += result
        logger.info(f"✅ OTX complete")
    except Exception as e:
        logger.error(f"❌ OTX error: {e}")
    
    # AbuseIPDB
    try:
        logger.info("📡 Fetching from AbuseIPDB...")
        result = abuseipdb.main()
        if result:
            total_new += result
        logger.info(f"✅ AbuseIPDB complete")
    except Exception as e:
        logger.error(f"❌ AbuseIPDB error: {e}")
    
    # Get total IOCs
    stats = db_manager.get_stats()
    total_iocs = stats.get('total', 0)
    
    logger.info("="*70)
    logger.info(f"✅ SCAN COMPLETE - New IOCs: {total_new} | Total: {total_iocs}")
    logger.info(f"⏰ Next scan in 30 minutes")
    logger.info("="*70)

def run_scheduler():
    """Run the scheduler"""
    logger.info("🚀 Real-Time IOC Scanner Starting...")
    logger.info("📊 Will scan every 30 minutes for fresh threat data")
    logger.info("Press Ctrl+C to stop\n")
    
    # Run immediately on start
    fetch_all_iocs()
    
    # Schedule to run every 30 minutes
    schedule.every(30).minutes.do(fetch_all_iocs)
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        logger.info("\n🛑 Real-time scanner stopped by user")
        sys.exit(0)
