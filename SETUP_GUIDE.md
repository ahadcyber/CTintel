# CTI Dashboard 🛠️ Setup Guide

**💡 Tip:** Skip setup entirely and use the live platform: [https://ctintel.onrender.com/](https://ctintel.onrender.com/)

---

## Local Installation:

## Quick Start Guide

Follow these steps to get your CTI Dashboard up and running.

### Step 1: Install MongoDB

**Windows:**
1. Download from [MongoDB Download Center](https://www.mongodb.com/try/download/community)
2. Run the installer
3. MongoDB will start automatically as a Windows service

**Verify Installation:**
```powershell
mongod --version
```

### Step 2: Set Up Python Environment

Open PowerShell in the project directory:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

Create a `.env` file:

```powershell
copy .env.example .env
```

Edit `.env` file with your settings:
```
MONGO_URI=mongodb://localhost:27017
OTX_API_KEY=your_key_here  # Optional
ABUSEIPDB_KEY=your_key_here  # Optional
```

**Getting API Keys (Optional but Recommended):**
- **OTX**: Sign up at https://otx.alienvault.com/ → Account Settings → API Integration
- **AbuseIPDB**: Register at https://www.abuseipdb.com/register → API → Copy key

### Step 4: Run the Application

```powershell
# Make sure MongoDB is running
# Then run:
run_all.bat
```

This will:
1. Fetch IOCs from all threat feeds
2. Store them in MongoDB
3. Launch the web dashboard

### Step 5: Access Dashboard

Open your browser and go to:
**http://127.0.0.1:5000**

---

## Manual Operations

### Run Individual Ingestors

```powershell
python ingestors\threatfox.py
python ingestors\phishtank.py
python ingestors\spamhaus.py
python ingestors\otx.py
python ingestors\abuseipdb.py
```

### Run Only the Dashboard

```powershell
python web\app.py
```

### Test API Endpoints

```powershell
# Get statistics
curl http://127.0.0.1:5000/api/stats

# Get IOCs
curl http://127.0.0.1:5000/api/iocs?limit=10

# Search IOCs
curl http://127.0.0.1:5000/api/search?q=malicious
```

---

## Troubleshooting

### MongoDB Connection Error

**Error:** `pymongo.errors.ServerSelectionTimeoutError`

**Solution:**
1. Check if MongoDB is running:
   ```powershell
   Get-Service MongoDB
   ```
2. Start MongoDB if stopped:
   ```powershell
   Start-Service MongoDB
   ```
3. Verify connection string in `.env`

### No Data Showing

**Solution:**
1. Run ingestors first: `run_all.bat`
2. Check MongoDB has data:
   ```powershell
   mongosh
   use cti_dashboard
   db.iocs.count()
   ```

### API Key Warnings

**Solution:**
- These are optional feeds
- Dashboard works without them
- Add keys in `.env` to enable all feeds

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
1. Find and kill the process:
   ```powershell
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```
2. Or change port in `web/app.py`

---

## Scheduling Automatic Updates

### Using Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Name: "CTI Dashboard Update"
4. Trigger: Daily at 2 AM
5. Action: Start a program
   - Program: `python`
   - Arguments: `ingestors\threatfox.py`
   - Start in: `C:\path\to\CTIntel`
6. Repeat for each ingestor

### Using Python APScheduler

Install scheduler:
```powershell
pip install apscheduler
```

Create `scheduler.py`:
```python
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', hours=6)
def update_feeds():
    subprocess.run(['run_all.bat'])

scheduler.start()
```

---

## Next Steps

- ✅ Set up scheduled updates
- ✅ Add more threat feeds
- ✅ Customize the dashboard
- ✅ Export IOCs to STIX format
- ✅ Add email alerts
- ✅ Deploy to cloud (AWS/Azure)

Happy Threat Hunting! 🔍
