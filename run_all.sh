#!/bin/bash

echo "======================================"
echo " CTI Dashboard - Starting All Services"
echo "======================================"
echo ""

echo "[1/6] Running ThreatFox Ingestor..."
python ingestors/threatfox.py
echo ""

echo "[2/6] Running PhishTank Ingestor..."
python ingestors/phishtank.py
echo ""

echo "[3/6] Running Spamhaus Ingestor..."
python ingestors/spamhaus.py
echo ""

echo "[4/6] Running AlienVault OTX Ingestor..."
python ingestors/otx.py
echo ""

echo "[5/6] Running AbuseIPDB Ingestor..."
python ingestors/abuseipdb.py
echo ""

echo "[6/6] Starting Flask Dashboard..."
echo "Dashboard will be available at: http://127.0.0.1:5000"
echo ""
python web/app.py
