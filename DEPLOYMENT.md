# 🚀 CTI Dashboard – Free Deployment Guide (Render + MongoDB Atlas)

**Live Example:** [https://ctintel.onrender.com/](https://ctintel.onrender.com/)

This guide explains how to host the **Cyber Threat Intelligence (CTI) Dashboard** online **for free** using  
**Render** (for the Flask web app) and **MongoDB Atlas** (for the database).

---

## 🧩 1. Requirements



| Item | Description |
|------|--------------|
| ✅ GitHub account | Your project code will be deployed from a GitHub repo |
| ✅ Render account | Free hosting platform for web services |
| ✅ MongoDB Atlas account | Free cloud database for storing IOCs |
| ✅ Python app ready | The CTI Dashboard source folder with `web/app.py` entry point |



---

## ☁️ 2. Step 1 – Push Project to GitHub

1. Create a new **GitHub repository** named `cti-dashboard`.
2. Upload all your files.
3. Commit & push the repo.

---

## 🛢️ 3. Step 2 – Set Up MongoDB Atlas (Free)

1. Go to [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Click **Start Free** → create an account.
3. Choose **Free Shared Cluster (M0)**.
4. Select a region near you (e.g., AWS → Mumbai / Singapore).
5. Create a database user:
   - Username: `ctiuser`
   - Password: `StrongPassword123!`
6. Click **Connect → Drivers → Python** and copy the URI.

   Example:
   ```
   mongodb+srv://ctiuser:StrongPassword123!@cluster0.xxxxx.mongodb.net/cti_dashboard
   ```
7. Save it — you'll paste it into Render later.

---

## 🧠 4. Step 3 – Deploy on Render (Free Web Service)

1. Go to [https://render.com](https://render.com)
2. Sign in → click **New +** → **Web Service**.
3. Connect your **GitHub repo** `cti-dashboard`.
4. Render detects it's a Python app.

**Configuration**

| Field | Value |
|--------|--------|
| **Name** | threatlens / cti-dashboard |
| **Region** | Closest to you |
| **Branch** | main |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python web/app.py` |

5. Click **Advanced → Add Environment Variables**:
   ```
   MONGO_URI = mongodb+srv://ctiuser:StrongPassword123!@cluster0.xxxxx.mongodb.net/cti_dashboard
   OTX_API_KEY = (optional)
   ABUSEIPDB_KEY = (optional)
   ```

6. Click **Deploy Web Service** 

Render will:
- Create a build environment
- Install dependencies
- Launch the Flask app

7. Wait until you see **"Build succeeded"** and **"Live"** status.

---

## 🌐 5. Step 4 – Access Your Live Dashboard

Once deployed, Render gives you a free HTTPS URL like:
```
https://cti-dashboard.onrender.com
```

Open that in your browser — your CTI Dashboard is now live! 🎉



---

## 🧪 6. Step 5 – Verify Data Ingestion

1. Open Render → **Shell tab** or deploy locally once to ingest data:
   ```bash
   python ingestors/threatfox.py
   python ingestors/phishtank.py
   python ingestors/spamhaus.py
   ```

2. Or use the web interface to manually trigger data collection.

3. Refresh your dashboard to see the IOCs populate.

---

## 📝 Notes

- **Free Tier Limits**: Render free tier sleeps after 15 minutes of inactivity. First request may take 30-60 seconds to wake up.
- **Database Size**: MongoDB Atlas free tier provides 512MB storage.
- **Automatic Updates**: Set up GitHub Actions or Render Cron Jobs to run ingestors periodically.

---

## 🎉 Success!

Your CTI Dashboard is now deployed and accessible from anywhere! 🌍

