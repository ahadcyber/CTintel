<div align="center">

# 🧠 Cyber Threat Intelligence (CTI) Dashboard

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-orange.svg)](https://github.com/yourusername/cti-dashboard/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**A lightweight, Python-based platform for aggregating and visualizing threat intelligence from free public feeds**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-project-structure) • [API](#-search-api-example) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

The **Cyber Threat Intelligence Dashboard** is an open-source, educational platform designed for security researchers, students, and analysts to collect, store, and analyze threat intelligence data without any cost.

### What It Does

- **Collect** - Automatically fetches Indicators of Compromise (IOCs) including malicious IPs, URLs, domains, and file hashes
- **Store** - Maintains a centralized MongoDB database for efficient querying and analytics
- **Visualize** - Provides an intuitive Flask-based web dashboard for threat analysis and exploration
- **Search** - Offers a RESTful API for quick IOC lookups and integrations

### Why Use This?

✅ **100% Free** - Uses only public APIs and open-source feeds  
✅ **Privacy-Focused** - Runs entirely on your local machine  
✅ **Educational** - Perfect for learning about threat intelligence workflows  
✅ **Extensible** - Easy to add new feeds or customize for your needs

---

## ⚙️ Features

| Feature | Description |
|---------|-------------|
| 🔄 **Automatic Feed Collection** | Fetches IOCs from ThreatFox, PhishTank, Spamhaus, OTX, and AbuseIPDB |
| 🗃️ **Centralized Storage** | All IOCs stored in MongoDB Atlas for querying and analytics |
| 📊 **Dashboard Visualization** | Displays counts by type/source, and lists the latest IOCs |
| 🔍 **Search API** | `/api/search?q=value` endpoint for quick IOC lookup |
| 🛡️ **Threat Lookup** | Interactive VirusTotal integration to verify IP/domain/URL/hash |
| 📈 **Trend Analysis** | Visualize IOC trends over time with interactive charts |
| 🏷️ **Tagging System** | Tag and categorize IOCs for better organization |
| 📥 **Export Functionality** | Export IOCs in CSV or JSON format for external analysis |
| 🔐 **Free & Ethical** | Uses only public/open-source CTI feeds; no paid APIs |
| ⚡ **Cloud-Ready** | Works locally or deploy to cloud with MongoDB Atlas |

---

## 🧰 Tech Stack

| Layer | Tools / Libraries |
|-------|-------------------|
| **Programming Language** | Python 3.8+ |
| **Framework** | Flask |
| **Database** | MongoDB (Local or MongoDB Atlas Free Tier) |
| **Visualization** | Chart.js (Browser) |
| **Data Sources (Feeds)** | ThreatFox, PhishTank, Spamhaus, AlienVault OTX, AbuseIPDB |
| **Other** | Requests, Dotenv, PyMongo |

---

## 📂 Project Structure

```
cti-dashboard/
├─ ingestors/
│  ├─ threatfox.py         # Pulls malware IOCs from Abuse.ch
│  ├─ otx.py               # AlienVault OTX open threat feeds
│  ├─ abuseipdb.py         # IP reputation via AbuseIPDB
│  ├─ phishtank.py         # Phishing URLs
│  └─ spamhaus.py          # Malicious IP ranges
│
├─ db/
│  └─ mongo.py             # MongoDB connection manager
│
├─ web/
│  ├─ app.py               # Flask dashboard application
│  └─ templates/
│     └─ dashboard.html    # UI template for viewing IOCs
│
├─ run_all.sh              # Linux/macOS script (fetch + launch)
├─ run_all.bat             # Windows version of the script
├─ requirements.txt        # Required dependencies
├─ .env.example            # Example environment config
└─ README.md               # Project documentation (this file)
```

---

## 📚 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **MongoDB** - [Installation guide](https://docs.mongodb.com/manual/installation/)
  - Alternatively, use [MongoDB Atlas Free Tier](https://www.mongodb.com/cloud/atlas/register)
- **Git** - [Download here](https://git-scm.com/downloads)

---

## 🔑 Environment Configuration

Create a `.env` file (based on `.env.example`) in your project root:

```bash
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/cti_dashboard
OTX_API_KEY=your_free_otx_key_here
ABUSEIPDB_KEY=your_free_abuseipdb_key_here
VIRUSTOTAL_API_KEY=your_free_virustotal_key_here
```

> ✅ **Note:** API keys are optional. The dashboard works with public feeds. VirusTotal key enables the interactive threat lookup feature.

**Getting API Keys (Optional):**
- **AlienVault OTX** - [Sign up here](https://otx.alienvault.com/)
- **AbuseIPDB** - [Get your key here](https://www.abuseipdb.com/register)
- **VirusTotal** - [Get your key here](https://www.virustotal.com/gui/join-us)

---

## 🧠 Threat Intelligence Feeds

| Feed | Data Type | Access | Notes |
|------|-----------|--------|-------|
| **ThreatFox** (abuse.ch) | IPs, Domains, Hashes | Public API | Malware IOCs from global submissions |
| **PhishTank** | URLs | Public CSV | Verified phishing links, updated daily |
| **Spamhaus DROP** | IP Ranges | Public TXT | Known spam/botnet networks |
| **AlienVault OTX** | IPs, Domains, Hashes | Free API Key | Global threat intelligence pulses |
| **AbuseIPDB** | IP Reputation | Free API Key | Rate-limited API for malicious IP reputation |
| **VirusTotal** | All Types | Free API Key | Interactive threat verification and analysis |

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/cti-dashboard.git
cd cti-dashboard
```

### 2️⃣ Set Up Virtual Environment

**Linux / macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment

Copy `.env.example` to `.env` and edit with your configuration:

```bash
cp .env.example .env  # Linux/macOS
copy .env.example .env  # Windows
```

### 5️⃣ Start the Dashboard

**Linux / macOS:**
```bash
chmod +x run_all.sh
./run_all.sh
```

**Windows:**
```powershell
run_all.bat
```

### 6️⃣ Access the Dashboard

Open your browser and navigate to:

👉 **http://127.0.0.1:5000**



---



🖥️ Dashboard Preview

Main Page:
- IOC count summary
- IOC breakdown by type and source
- Latest 100 IOCs
- Simple search API endpoint

---

🔍 Search API Example

**GET** `/api/search?q=google`

Response Example:
```json
[
  {
    "_id": "652a4c9e5e8b3e20b6f91c0b",
    "value": "malicious-domain.com",
    "type": "domain",
    "source": "ThreatFox"
  }
]
```





---

🧩 Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `pymongo.errors.ServerSelectionTimeoutError` | MongoDB not running | Start MongoDB service (mongod) |
| API key missing warnings | Optional feeds skipped | Add keys in .env |
| Dashboard shows no data | Feeds not ingested | Run run_all.sh or ingestors manually |







---

🛡️ Ethical & Legal Use

- Respect API rate limits and Terms of Service for each data provider.
- Always use the data within your own lab or authorized environment.

---

🧠 Future Enhancements

- [ ] Add GeoIP lookup & country flags for IPs
- [ ] Add user login (Flask-Login)
- [ ] Automate ingestion via scheduler (e.g., cron or apscheduler)
- [ ] Docker Compose support
- [ ] Export data in STIX 2.1 format







---

👨‍💻 Author

**Project By:** Abdul Ahad  
**Focus:** Cybersecurity | Threat Intelligence | Software Development  
**Version:** 1.0 (Free Local Edition)

