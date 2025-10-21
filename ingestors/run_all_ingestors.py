"""
Run all IOC ingestors in sequence
Useful for scheduled jobs and automated updates
"""
import sys
import os
import logging
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_ingestor(ingestor_name):
    """Run a single ingestor"""
    try:
        logger.info(f"Starting {ingestor_name}...")
        module = __import__(ingestor_name)
        if hasattr(module, 'main'):
            module.main()
        logger.info(f"✅ {ingestor_name} completed")
        return True
    except Exception as e:
        logger.error(f"❌ {ingestor_name} failed: {e}")
        return False

def main():
    """Run all ingestors"""
    logger.info("="*60)
    logger.info(f"🚀 Starting IOC ingestion - {datetime.now()}")
    logger.info("="*60)
    
    ingestors = [
        'threatfox',
        'phishtank',
        'spamhaus',
        'otx',
        'abuseipdb'
    ]
    
    results = {}
    for ingestor in ingestors:
        results[ingestor] = run_ingestor(ingestor)
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("📊 Ingestion Summary")
    logger.info("="*60)
    
    successful = sum(1 for v in results.values() if v)
    failed = len(results) - successful
    
    for ingestor, success in results.items():
        status = "✅ Success" if success else "❌ Failed"
        logger.info(f"{ingestor:20s}: {status}")
    
    logger.info(f"\n✅ Successful: {successful}/{len(results)}")
    if failed > 0:
        logger.info(f"❌ Failed: {failed}/{len(results)}")
    
    logger.info("="*60)
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
