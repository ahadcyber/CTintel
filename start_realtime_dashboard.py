"""
Start Real-Time CTI Dashboard with automatic IOC updates
This runs both the web server and background scanner
"""
import subprocess
import sys
import os
import time
from threading import Thread
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_web_server():
    """Run Flask web server"""
    logger.info("🌐 Starting Web Server...")
    subprocess.run([sys.executable, 'web/app.py'], cwd=os.getcwd())

def run_realtime_scanner():
    """Run real-time IOC scanner"""
    time.sleep(5)  # Wait for web server to start
    logger.info("📡 Starting Real-Time Scanner...")
    subprocess.run([sys.executable, 'realtime_scanner.py'], cwd=os.getcwd())

if __name__ == "__main__":
    print("="*70)
    print("🧠 REAL-TIME CYBER THREAT INTELLIGENCE DASHBOARD")
    print("="*70)
    print()
    print("✅ Web Dashboard: http://127.0.0.1:5000")
    print("✅ Auto-scanning: Every 30 minutes")
    print("✅ Live threat feeds: ThreatFox, PhishTank, Spamhaus, OTX, AbuseIPDB")
    print()
    print("Press Ctrl+C to stop both services")
    print("="*70)
    print()
    
    try:
        # Start web server in a thread
        web_thread = Thread(target=run_web_server, daemon=True)
        web_thread.start()
        
        # Run scanner in main thread (so Ctrl+C works)
        run_realtime_scanner()
        
    except KeyboardInterrupt:
        logger.info("\n🛑 Shutting down Real-Time Dashboard...")
        sys.exit(0)
