# 📖 CTI Dashboard - API Documentation

**Live Platform:** [https://ctintel.onrender.com/](https://ctintel.onrender.com/)

Complete API reference for the Cyber Threat Intelligence Dashboard by **Abdul Ahad Rasool** v2.0

---

## 🌐 Base URL

```
Local:      http://127.0.0.1:5000
Production: https://ctintel.onrender.com
```

**🎯 Try it live:** All endpoints below work at [https://ctintel.onrender.com](https://ctintel.onrender.com)

---

## 🔐 Authentication

Currently, the API is open. Future versions will include API key authentication.

---

## 📊 Endpoints

### 1. Health Check

Check service health and database connectivity.

```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "database": "connected",
  "timestamp": "2025-10-17T15:30:00.000Z"
}
```

**Status Codes:**
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service is unhealthy

---

### 2. Get Statistics

Retrieve IOC statistics including counts by type and source.

```http
GET /api/stats
```

**Rate Limit:** 60 requests/minute  
**Cache:** 60 seconds

**Response:**
```json
{
  "total": 2286,
  "by_type": [
    {"_id": "ip_range", "count": 1475},
    {"_id": "url", "count": 779},
    {"_id": "domain", "count": 12}
  ],
  "by_source": [
    {"_id": "Spamhaus", "count": 1480},
    {"_id": "PhishTank", "count": 784}
  ]
}
```

**Example:**
```bash
curl http://127.0.0.1:5000/api/stats
```

---

### 3. Get IOCs

Retrieve IOCs with pagination and filtering.

```http
GET /api/iocs?limit=100&skip=0&type=url&source=PhishTank
```

**Rate Limit:** 100 requests/minute

**Query Parameters:**
| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `limit` | integer | 100 | 1000 | Number of IOCs to return |
| `skip` | integer | 0 | - | Number of IOCs to skip (pagination) |
| `type` | string | - | - | Filter by IOC type (ip, url, domain, hash, ip_range) |
| `source` | string | - | - | Filter by source name |

**Response:**
```json
{
  "iocs": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "value": "http://malicious-site.com",
      "type": "url",
      "source": "PhishTank",
      "timestamp": {"$date": "2025-10-17T15:30:00.000Z"}
    }
  ],
  "total": 784,
  "limit": 100,
  "skip": 0
}
```

**Examples:**
```bash
# Get latest 10 IOCs
curl "http://127.0.0.1:5000/api/iocs?limit=10"

# Get URLs only
curl "http://127.0.0.1:5000/api/iocs?type=url&limit=50"

# Get IOCs from specific source
curl "http://127.0.0.1:5000/api/iocs?source=ThreatFox"

# Pagination (page 2, 100 per page)
curl "http://127.0.0.1:5000/api/iocs?skip=100&limit=100"
```

---

### 4. Search IOCs

Search for IOCs by value (supports regex).

```http
GET /api/search?q=malware&limit=50
```

**Rate Limit:** 30 requests/minute

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | Search query (supports partial matching) |
| `limit` | integer | No | Maximum results (default: 50, max: 100) |

**Response:**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "value": "http://malware-download.com/payload.exe",
    "type": "url",
    "source": "ThreatFox",
    "timestamp": {"$date": "2025-10-17T15:30:00.000Z"}
  }
]
```

**Examples:**
```bash
# Search for IP address
curl "http://127.0.0.1:5000/api/search?q=192.168"

# Search for domain
curl "http://127.0.0.1:5000/api/search?q=malicious.com"

# Search for hash
curl "http://127.0.0.1:5000/api/search?q=d41d8cd98f00b204e9800998ecf8427e"

# Search with limit
curl "http://127.0.0.1:5000/api/search?q=phishing&limit=20"
```

---

### 5. Export IOCs

Export IOCs in CSV or JSON format.

```http
GET /api/export/{format}?type=url&source=PhishTank&limit=1000
```

**Rate Limit:** 5 requests/hour

**Path Parameters:**
| Parameter | Type | Options | Description |
|-----------|------|---------|-------------|
| `format` | string | csv, json | Export format |

**Query Parameters:**
| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `type` | string | - | - | Filter by IOC type |
| `source` | string | - | - | Filter by source |
| `limit` | integer | 1000 | 10000 | Maximum records |

**Response:**
- CSV: `text/csv` file download
- JSON: `application/json` file download

**Examples:**
```bash
# Export all IOCs as JSON
curl "http://127.0.0.1:5000/api/export/json" -O

# Export URLs as CSV
curl "http://127.0.0.1:5000/api/export/csv?type=url" -O

# Export from specific source
curl "http://127.0.0.1:5000/api/export/json?source=PhishTank" -O

# Export limited records
curl "http://127.0.0.1:5000/api/export/csv?limit=500" -O
```

---

### 6. Get Sources

List all available IOC sources.

```http
GET /api/sources
```

**Rate Limit:** Unlimited  
**Cache:** 300 seconds

**Response:**
```json
{
  "sources": [
    "ThreatFox",
    "PhishTank",
    "Spamhaus",
    "AlienVault OTX",
    "AbuseIPDB"
  ]
}
```

**Example:**
```bash
curl http://127.0.0.1:5000/api/sources
```

---

### 7. Get IOC Types

List all available IOC types.

```http
GET /api/types
```

**Rate Limit:** Unlimited  
**Cache:** 300 seconds

**Response:**
```json
{
  "types": [
    "ip",
    "url",
    "domain",
    "hash",
    "ip_range"
  ]
}
```

**Example:**
```bash
curl http://127.0.0.1:5000/api/types
```

---

### 8. Get Configuration

Get public application configuration.

```http
GET /api/config
```

**Response:**
```json
{
  "app_name": "CTI Dashboard",
  "version": "2.0.0",
  "environment": "production",
  "features": {
    "export": true,
    "api_docs": true,
    "rate_limiting": true
  },
  "pagination": {
    "default_page_size": 100,
    "max_page_size": 1000
  }
}
```

---

## 🛡️ Rate Limiting

Rate limits are enforced per IP address:

| Endpoint | Rate Limit |
|----------|------------|
| `/api/stats` | 60/minute |
| `/api/iocs` | 100/minute |
| `/api/search` | 30/minute |
| `/api/export/*` | 5/hour |
| `/api/sources` | Unlimited |
| `/api/types` | Unlimited |
| `/api/health` | Unlimited |
| `/api/config` | Unlimited |

**Rate Limit Headers:**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1634486400
```

**Rate Limit Exceeded Response:**
```json
{
  "error": "Rate limit exceeded",
  "message": "100 per 1 minute"
}
```

**Status Code:** `429 Too Many Requests`

---

## 📝 Response Formats

### Success Response

```json
{
  "data": [...],
  "metadata": {...}
}
```

### Error Response

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### Common Status Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `400` | Bad Request (invalid parameters) |
| `404` | Not Found |
| `429` | Rate Limit Exceeded |
| `500` | Internal Server Error |
| `503` | Service Unavailable |

---

## 🔧 Pagination

Use `limit` and `skip` parameters for pagination:

```bash
# Page 1 (first 100)
curl "http://127.0.0.1:5000/api/iocs?limit=100&skip=0"

# Page 2 (next 100)
curl "http://127.0.0.1:5000/api/iocs?limit=100&skip=100"

# Page 3 (next 100)
curl "http://127.0.0.1:5000/api/iocs?limit=100&skip=200"
```

**Calculate skip:**
```
skip = (page_number - 1) * limit
```

---

## 🐍 Python Examples

### Basic Usage

```python
import requests

BASE_URL = "http://127.0.0.1:5000"

# Get statistics
response = requests.get(f"{BASE_URL}/api/stats")
stats = response.json()
print(f"Total IOCs: {stats['total']}")

# Search for IOC
response = requests.get(f"{BASE_URL}/api/search", params={"q": "malware"})
results = response.json()
print(f"Found {len(results)} results")

# Get filtered IOCs
response = requests.get(f"{BASE_URL}/api/iocs", params={
    "type": "url",
    "source": "PhishTank",
    "limit": 10
})
iocs = response.json()
print(f"Retrieved {len(iocs['iocs'])} IOCs")
```

### Export Data

```python
import requests

BASE_URL = "http://127.0.0.1:5000"

# Export as JSON
response = requests.get(f"{BASE_URL}/api/export/json")
with open("iocs_export.json", "wb") as f:
    f.write(response.content)

# Export as CSV
response = requests.get(f"{BASE_URL}/api/export/csv", params={"type": "url"})
with open("urls_export.csv", "wb") as f:
    f.write(response.content)
```

### With Error Handling

```python
import requests

BASE_URL = "http://127.0.0.1:5000"

try:
    response = requests.get(f"{BASE_URL}/api/search", params={"q": "malware"})
    response.raise_for_status()  # Raise exception for 4xx/5xx
    
    results = response.json()
    for ioc in results:
        print(f"{ioc['value']} ({ioc['type']})")
        
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 429:
        print("Rate limit exceeded. Please wait.")
    else:
        print(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

---

## 🌐 JavaScript/cURL Examples

### JavaScript (Fetch API)

```javascript
const BASE_URL = 'http://127.0.0.1:5000';

// Get statistics
fetch(`${BASE_URL}/api/stats`)
  .then(response => response.json())
  .then(data => console.log('Total IOCs:', data.total))
  .catch(error => console.error('Error:', error));

// Search IOCs
async function searchIOCs(query) {
  const response = await fetch(`${BASE_URL}/api/search?q=${encodeURIComponent(query)}`);
  if (!response.ok) {
    throw new Error(`HTTP error ${response.status}`);
  }
  return await response.json();
}

// Usage
searchIOCs('malware').then(results => {
  console.log(`Found ${results.length} results`);
});
```

### cURL Examples

```bash
# Get stats with pretty JSON
curl -s http://127.0.0.1:5000/api/stats | jq

# Search with headers
curl -H "Accept: application/json" \
     "http://127.0.0.1:5000/api/search?q=malware"

# Export with authentication (if enabled)
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "http://127.0.0.1:5000/api/export/json" \
     -o export.json

# Check response headers
curl -I http://127.0.0.1:5000/api/health
```

---

## 📚 Interactive Documentation

Visit `/api/docs` on your running instance for interactive Swagger UI documentation where you can:

- 📖 Browse all endpoints
- 🧪 Test API calls directly
- 📝 View request/response schemas
- 🔍 See example responses

---

## 🤝 Support

For API issues or questions:
- 📧 GitHub Issues
- 💬 API Discussion Forum
- 📖 Full Documentation

---

**Last Updated:** October 2025  
**API Version:** 2.0.0
