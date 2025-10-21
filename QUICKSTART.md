# 🚀 Quick Start - CTI Dashboard

Get your CTI Dashboard running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] MongoDB installed and running
- [ ] Git installed (optional)

---

## Installation Steps

### 1. Install MongoDB (if not installed)

**Download:** https://www.mongodb.com/try/download/community

After installation, verify:
```powershell
mongod --version
```

### 2. Set Up Project

Open PowerShell in the `CTIntel` directory:

```powershell
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```powershell
# Create .env file from template
copy .env.example .env

# Edit .env (optional - works without API keys)
notepad .env
```

### 4. Run the Dashboard

```powershell
run_all.bat
```

**That's it!** Open your browser: http://127.0.0.1:5000

---

## What Happens When You Run It?

1. **ThreatFox** - Fetches malware IOCs (IPs, domains, hashes)
2. **PhishTank** - Collects phishing URLs
3. **Spamhaus** - Gets malicious IP ranges
4. **AlienVault OTX** - Pulls threat pulses (requires API key)
5. **AbuseIPDB** - Retrieves bad IPs (requires API key)
6. **Dashboard** - Launches at http://127.0.0.1:5000

---

## Troubleshooting

### MongoDB Not Running?
```powershell
# Check status
Get-Service MongoDB

# Start if stopped
Start-Service MongoDB
```

### Port 5000 Already in Use?
Edit `web/app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### No Data Showing?
Wait 30-60 seconds for ingestors to complete, then refresh the dashboard.

---

## Optional API Keys

**AlienVault OTX:** https://otx.alienvault.com/ (free signup)
**AbuseIPDB:** https://www.abuseipdb.com/register (free tier)

Add them to `.env`:
```
OTX_API_KEY=your_key_here
ABUSEIPDB_KEY=your_key_here
```

---

## Next Steps

✅ **Explore the Dashboard** - View IOC statistics and charts
✅ **Try the Search** - Search for specific IPs, domains, or URLs
✅ **Test the API** - Use `/api/search?q=malicious`
✅ **Schedule Updates** - Set up automatic feed refresh (see SETUP_GUIDE.md)

**Need Help?** Check SETUP_GUIDE.md for detailed instructions!

Happy Threat Hunting! 🔍🛡️
