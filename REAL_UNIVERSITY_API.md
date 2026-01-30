# Real University Data Integration Guide

##  **Integrated API: Universities Hipolabs**

We've integrated a **free, open-source API** with **10,000+ real universities** worldwide!

**API:** http://universities.hipolabs.com/
-  **Free** - No API key needed
-  **10,000+ universities** from 200+ countries
-  **Real data** - Names, countries, websites
-  **No rate limits**
-  **JSON format**

---

##  **How to Use**

### **Option 1: Import Real Universities** (Recommended)

Import actual universities from the API into your database:

```bash
# Start your backend
uvicorn main:app --reload
```

**Then visit in browser or use curl:**

```bash
# Import universities from default countries (US, UK, Canada, Germany, Australia)
http://localhost:8000/api/universities/import-real

# Or with specific countries (POST request)
curl -X POST "http://localhost:8000/api/universities/import-real" \
  -H "Content-Type: application/json" \
  -d '{"countries": ["United States", "United Kingdom", "India", "Canada"]}'
```

This will:
- Fetch real universities from each country
- Import up to 30 universities per country
- Save to your database
- Add realistic tuition estimates
- Set requirements based on country

**Response:**
```json
{
  "message": "Successfully imported 120 real universities",
  "countries": ["United States", "United Kingdom", "India", "Canada"]
}
```

---

### **Option 2: Search API Directly** (Real-time)

Search universities in real-time without storing in database:

```bash
# Search by country
http://localhost:8000/api/universities/search-api?country=United States

# Search by university name
http://localhost:8000/api/universities/search-api?name=Harvard
```

**Response:**
```json
{
  "count": 50,
  "universities": [
    {
      "name": "Harvard University",
      "country": "United States",
      "web_pages": ["http://www.harvard.edu"],
      "domains": ["harvard.edu"]
    },
    ...
  ]
}
```

---

### **Option 3: Sample Data** (Quick Start)

Use pre-seeded sample data (MIT, Stanford, etc.):

```bash
http://localhost:8000/api/universities/seed
```

---

##  **Recommended Workflow**

### **For Development:**
```bash
# 1. Use sample data for quick testing
http://localhost:8000/api/universities/seed

# 2. Test your features with 10 universities
```

### **For Demo/Production:**
```bash
# Import real universities from your target countries
POST http://localhost:8000/api/universities/import-real
{
  "countries": [
    "United States",
    "United Kingdom", 
    "Canada",
    "Germany",
    "Australia",
    "India",
    "Singapore"
  ]
}

# This gives you 200+ real universities!
```

---

##  **Available Countries**

The API supports universities from:

### **Popular Study Destinations:**
- United States (1000+ universities)
- United Kingdom (200+ universities)
- Canada (100+ universities)
- Australia (50+ universities)
- Germany (200+ universities)
- Netherlands (50+ universities)
- France (100+ universities)
- Singapore (10+ universities)
- India (500+ universities)
- China (300+ universities)
- Japan (100+ universities)

### **Full List:**
200+ countries available! Check: http://universities.hipolabs.com/search?country=

---

##  **How It Works**

### **1. API Call**
```python
# Fetch universities by country
GET http://universities.hipolabs.com/search?country=United States

# Response:
[
  {
    "name": "Massachusetts Institute of Technology",
    "country": "United States",
    "alpha_two_code": "US",
    "web_pages": ["http://web.mit.edu"],
    "domains": ["mit.edu"]
  },
  ...
]
```

### **2. Data Transformation**
We enhance the API data with:
- **Tuition estimates** (based on country averages)
- **Acceptance rates** (realistic estimates)
- **Programs offered** (common programs)
- **Requirements** (IELTS, GRE, GPA)
- **Fields of study** (CS, Engineering, Business, etc.)

### **3. Storage**
Transformed data is saved to your database in the `universities` table.

---

##  **Pro Tips**

### **1. Smart Import**
Import only countries your users care about:

```python
# In Swagger UI or Postman
POST /api/universities/import-real
{
  "countries": ["United States", "United Kingdom", "Canada"]
}
```

### **2. Refresh Data**
Re-import to update:
```bash
# The system checks for duplicates
# Only new universities are added
POST /api/universities/import-real
```

### **3. Mix Sample + Real Data**
```bash
# 1. Seed sample universities (for well-known ones)
GET /api/universities/seed

# 2. Import real universities (for comprehensive list)
POST /api/universities/import-real
```

---

##  **Enhanced Features**

### **Country-Specific Tuition Estimates**

| Country | Tuition Range (USD/year) |
|---------|-------------------------|
| USA | $30,000 - $60,000 |
| UK | $20,000 - $40,000 |
| Canada | $15,000 - $35,000 |
| Germany | $0 - $3,000 |
| Australia | $20,000 - $45,000 |
| Netherlands | $8,000 - $20,000 |
| France | $2,000 - $15,000 |
| India | $2,000 - $10,000 |

### **Automatic Requirements**

Based on country:
- **IELTS**: 6.5 (English-speaking countries) or 6.0 (others)
- **GRE**: 300 (USA/Canada) or not required
- **GPA**: 3.0 minimum

---

##  **Testing the Integration**

### **Test 1: Import Real Universities**
```bash
# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/universities/import-real" -Method Post
```

### **Test 2: Search API**
```bash
# Browser
http://localhost:8000/api/universities/search-api?country=Germany
```

### **Test 3: Get Recommendations**
```bash
# After login
http://localhost:8000/api/universities/recommendations
```

---

##  **What You Get**

### **Real University Examples:**

**United States:**
- Harvard University
- Stanford University
- MIT
- Yale University
- Columbia University
- ... (1000+ more)

**United Kingdom:**
- University of Oxford
- University of Cambridge
- Imperial College London
- UCL
- ... (200+ more)

**Germany:**
- Technical University of Munich
- LMU Munich
- Heidelberg University
- ... (200+ more)

---

##  **Scalability**

### **Current Setup:**
- Import 30 universities per country
- 5 countries = 150 universities
- Perfect for hackathon/demo

### **Scale Up:**
```python
# Import more per country
import_universities_from_api(db, countries, limit_per_country=100)

# Import from more countries
countries = ["United States", "UK", "Canada", "Germany", 
             "Australia", "Netherlands", "France", "Sweden"]
```

---

##  **Advanced Usage**

### **Search by Name**
```bash
http://localhost:8000/api/universities/search-api?name=University of California
```

Returns all UC campuses!

### **Combine with Your Algorithm**
The imported universities work seamlessly with your existing:
- Profile matching
- Dream/Target/Safe categorization
- Budget filtering
- AI recommendations

---

## ️ **Limitations**

### **API Data Includes:**
-  University name
-  Country
-  Website
-  Domain

### **We Add (Estimates):**
- Tuition fees (country averages)
- Acceptance rates (estimates)
- Programs (common ones)
- Requirements (standard)
- City (not available in API)
- Rankings (not available in API)

For more detailed data, you can:
1. Manually curate top universities
2. Use additional APIs (QS Rankings API, etc.)
3. Web scraping (requires more setup)

---

##  **Recommendation**

**For your hackathon:**

1. **Use Sample Data** for top universities (MIT, Harvard, etc.)
   ```bash
   GET /api/universities/seed
   ```

2. **Import Real Data** for comprehensive list
   ```bash
   POST /api/universities/import-real
   ```

3. **Show both** in your demo:
   - "We have 200+ real universities from the Hipolabs API"
   - "Including all top universities with detailed data"

This shows:
-  Real API integration
-  Production-ready approach
-  Scalable solution

---

##  **Get Started Now**

```bash
# Start backend
cd backend
uvicorn main:app --reload

# In browser or new terminal:
# Import real universities
curl -X POST http://localhost:8000/api/universities/import-real

# View in Swagger UI
http://localhost:8000/docs
```

**That's it!** You now have real university data from a free API! 
