# 🚀 CTI Dashboard - Production Deployment Guide

Complete guide for deploying CTI Dashboard to production environments.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Deployment Options](#deployment-options)
  - [Docker Deployment](#docker-deployment)
  - [Heroku](#heroku)
  - [AWS (Elastic Beanstalk)](#aws-elastic-beanstalk)
  - [Azure Web Apps](#azure-web-apps)
  - [Google Cloud Run](#google-cloud-run)
  - [Railway](#railway)
  - [Render](#render)
- [Post-Deployment](#post-deployment)
- [Monitoring](#monitoring)

---

## Prerequisites

### Required
- ✅ Python 3.9 or higher
- ✅ MongoDB Atlas account (or self-hosted MongoDB)
- ✅ Git

### Optional API Keys
- 🔑 AlienVault OTX API key
- 🔑 AbuseIPDB API key

---

## Configuration

### 1. Environment Variables

Create or update your `.env` file:

```bash
# MongoDB Configuration
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/

# Flask Configuration
FLASK_ENV=production
PORT=5000
SECRET_KEY=your-secret-key-here

# Optional API Keys
OTX_API_KEY=your-otx-key
ABUSEIPDB_KEY=your-abuseipdb-key

# Features
ENABLE_EXPORT=true
ENABLE_API_DOCS=true
RATELIMIT_ENABLED=true

# Logging
LOG_LEVEL=INFO
```

### 2. Generate Secret Key

```bash
python -c "import os; print(os.urandom(24).hex())"
```

---

## Deployment Options

### 🐳 Docker Deployment

#### Build and Run Locally

```bash
# Build image
docker build -t cti-dashboard .

# Run container (with Atlas)
docker run -d \
  -p 5000:5000 \
  -e MONGO_URI="your-mongodb-uri" \
  --name cti-dashboard \
  cti-dashboard
```

#### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Push to Docker Hub

```bash
# Tag image
docker tag cti-dashboard yourusername/cti-dashboard:latest

# Push
docker push yourusername/cti-dashboard:latest
```

---

### 🟣 Heroku

#### Step 1: Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
heroku --version
```

#### Step 2: Login and Create App
```bash
heroku login
heroku create your-cti-dashboard
```

#### Step 3: Add MongoDB Atlas
```bash
# Set MongoDB URI
heroku config:set MONGO_URI="your-mongodb-atlas-uri"
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set FLASK_ENV=production
```

#### Step 4: Create Procfile
Create `Procfile` in project root:
```
web: gunicorn wsgi:application
```

#### Step 5: Deploy
```bash
git add .
git commit -m "Production deployment"
git push heroku main
```

#### Step 6: Scale
```bash
heroku ps:scale web=1
heroku open
```

---

### ☁️ AWS (Elastic Beanstalk)

#### Step 1: Install EB CLI
```bash
pip install awsebcli
eb --version
```

#### Step 2: Initialize
```bash
eb init -p python-3.11 cti-dashboard --region us-east-1
```

#### Step 3: Create Environment
```bash
eb create cti-dashboard-prod
```

#### Step 4: Set Environment Variables
```bash
eb setenv MONGO_URI="your-mongodb-uri" \
  SECRET_KEY="your-secret-key" \
  FLASK_ENV=production
```

#### Step 5: Deploy
```bash
eb deploy
eb open
```

---

### 🔵 Azure Web Apps

#### Step 1: Install Azure CLI
```bash
# Download from https://docs.microsoft.com/cli/azure/install-azure-cli
az --version
```

#### Step 2: Login
```bash
az login
```

#### Step 3: Create Resources
```bash
# Create resource group
az group create --name cti-rg --location eastus

# Create App Service plan
az appservice plan create \
  --name cti-plan \
  --resource-group cti-rg \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group cti-rg \
  --plan cti-plan \
  --name your-cti-dashboard \
  --runtime "PYTHON:3.11"
```

#### Step 4: Configure Environment
```bash
az webapp config appsettings set \
  --resource-group cti-rg \
  --name your-cti-dashboard \
  --settings \
    MONGO_URI="your-mongodb-uri" \
    SECRET_KEY="your-secret-key" \
    FLASK_ENV=production \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

#### Step 5: Deploy
```bash
az webapp up \
  --resource-group cti-rg \
  --name your-cti-dashboard \
  --runtime "PYTHON:3.11"
```

---

### 🟡 Google Cloud Run

#### Step 1: Install gcloud CLI
```bash
# Download from https://cloud.google.com/sdk/docs/install
gcloud --version
```

#### Step 2: Initialize and Login
```bash
gcloud init
gcloud auth login
```

#### Step 3: Build Container
```bash
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/cti-dashboard
```

#### Step 4: Deploy
```bash
gcloud run deploy cti-dashboard \
  --image gcr.io/YOUR-PROJECT-ID/cti-dashboard \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MONGO_URI="your-mongodb-uri" \
  --set-env-vars SECRET_KEY="your-secret-key" \
  --set-env-vars FLASK_ENV=production
```

---

### 🚂 Railway

#### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
railway login
```

#### Step 2: Initialize Project
```bash
railway init
```

#### Step 3: Add MongoDB
```bash
railway add mongodb
```

#### Step 4: Set Variables
```bash
railway variables set MONGO_URI="your-mongodb-uri"
railway variables set SECRET_KEY="your-secret-key"
railway variables set FLASK_ENV=production
```

#### Step 5: Deploy
```bash
railway up
railway open
```

---

### 🎨 Render

#### Via Web Dashboard:

1. **Go to [render.com](https://render.com)**
2. **Connect your GitHub repository**
3. **Create New Web Service**
4. **Configure:**
   - **Name**: cti-dashboard
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:application`
5. **Add Environment Variables:**
   - `MONGO_URI`
   - `SECRET_KEY`
   - `FLASK_ENV=production`
6. **Deploy**

#### Via render.yaml:

Create `render.yaml`:
```yaml
services:
  - type: web
    name: cti-dashboard
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn wsgi:application
    envVars:
      - key: MONGO_URI
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: FLASK_ENV
        value: production
```

---

## Post-Deployment

### 1. Verify Deployment

```bash
# Check health
curl https://your-app-url.com/api/health

# Check stats
curl https://your-app-url.com/api/stats
```

### 2. Populate Data

```bash
# SSH into server or run locally pointing to production DB
python ingestors/threatfox.py
python ingestors/phishtank.py
python ingestors/spamhaus.py
```

### 3. Set Up Scheduled Jobs

#### Heroku Scheduler
```bash
heroku addons:create scheduler:standard
heroku addons:open scheduler
```
Add job: `python ingestors/run_all_ingestors.py`

#### AWS CloudWatch Events
Create EventBridge rule to trigger Lambda/ECS task

#### Railway Cron
Add to `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "healthcheckPath": "/api/health"
  }
}
```

---

## Monitoring

### Application Monitoring

```bash
# View logs
heroku logs --tail  # Heroku
docker logs -f cti-dashboard  # Docker
railway logs  # Railway
```

### Setup Uptime Monitoring

Use services like:
- **UptimeRobot** (free)
- **Pingdom**
- **StatusCake**

Monitor: `https://your-app.com/api/health`

### Database Monitoring

MongoDB Atlas provides built-in monitoring:
- Performance metrics
- Query analytics
- Alerts

---

## Security Checklist

- ✅ Use HTTPS (enabled by most platforms)
- ✅ Set strong SECRET_KEY
- ✅ Enable rate limiting
- ✅ Whitelist MongoDB Atlas IP addresses
- ✅ Use environment variables (never commit secrets)
- ✅ Regular dependency updates
- ✅ Enable logging
- ✅ Set up monitoring alerts

---

## Performance Optimization

### 1. Database Indexes
Already created in `db/mongo.py`:
- `value` index
- `type` index
- `source` index
- `timestamp` index

### 2. Caching
Enabled by default with Flask-Caching

### 3. CDN (Optional)
Use CloudFlare or similar for static assets

### 4. Scaling
- **Horizontal**: Add more worker processes
- **Vertical**: Increase memory/CPU

---

## Troubleshooting

### Issue: App not starting
**Solution**: Check logs for errors, verify environment variables

### Issue: Database connection timeout
**Solution**: Check MongoDB Atlas IP whitelist (add 0.0.0.0/0 for all IPs)

### Issue: High memory usage
**Solution**: Reduce worker count or increase instance size

### Issue: Slow API responses
**Solution**: Check database indexes, enable caching

---

## Support

For issues, see:
- 📧 GitHub Issues
- 📚 Documentation
- 💬 Community Support

---

**Happy Deploying! 🚀**
