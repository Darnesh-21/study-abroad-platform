# Backend Setup Guide

## Installation Steps

### 1. Install Python Dependencies

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Setup PostgreSQL

#### Option A: Local PostgreSQL
```bash
# Install PostgreSQL (Windows: https://www.postgresql.org/download/windows/)
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql

# Create database
createdb study_abroad_db
```

#### Option B: Docker PostgreSQL
```bash
docker run --name postgres-study-abroad -e POSTGRES_PASSWORD=password -e POSTGRES_DB=study_abroad_db -p 5432:5432 -d postgres:14
```

### 3. Configure Environment

Create `.env` file:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/study_abroad_db
SECRET_KEY=your-secret-key-change-this-in-production
GEMINI_API_KEY=your-gemini-api-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Get Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy and paste into .env file

### 5. Run Backend

```bash
uvicorn main:app --reload
```

API will be available at: http://localhost:8000

### 6. Verify Setup

Open browser:
- http://localhost:8000 - Should show API status
- http://localhost:8000/docs - Interactive API documentation

### 7. Seed Database

```bash
# Visit in browser:
http://localhost:8000/api/universities/seed
```

## API Documentation

FastAPI provides automatic interactive documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing APIs

You can test the APIs using:
1. Swagger UI at /docs
2. Postman
3. cURL commands

Example:
```bash
# Signup
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Test User", "email": "test@example.com", "password": "password123"}'
```

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── app/
    ├── __init__.py
    ├── config.py        # Configuration
    ├── database.py      # Database connection
    ├── models.py        # SQLAlchemy models
    ├── schemas.py       # Pydantic schemas
    ├── auth_utils.py    # Authentication utilities
    └── api/             # API routes
        ├── auth.py
        ├── onboarding.py
        ├── dashboard.py
        ├── profile.py
        ├── universities.py
        ├── todos.py
        └── counselor.py
```

## Common Issues

### Database Connection Failed
```bash
# Check PostgreSQL is running
# Windows: Check Services
# Mac: brew services start postgresql
# Linux: sudo service postgresql start
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Port Already in Use
```bash
# Run on different port
uvicorn main:app --reload --port 8001
```

## Production Deployment

For production deployment:

1. Update SECRET_KEY to a strong random value
2. Use production database
3. Set up proper CORS origins
4. Use gunicorn:

```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
