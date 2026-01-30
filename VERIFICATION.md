# Setup Verification Script

## Quick Health Check

Use this guide to verify your setup is working correctly.

## Backend Verification

### 1. Check Backend is Running
Open browser: http://localhost:8000

**Expected Response:**
```json
{
  "message": "Study Abroad Platform API",
  "status": "running"
}
```

### 2. Check API Documentation
Open: http://localhost:8000/docs

**Expected:** Interactive Swagger UI with all endpoints listed

### 3. Check Health Endpoint
Open: http://localhost:8000/health

**Expected Response:**
```json
{
  "status": "healthy"
}
```

### 4. Verify Database Connection
Run a test signup through Swagger UI:

1. Go to http://localhost:8000/docs
2. Find `POST /api/auth/signup`
3. Click "Try it out"
4. Enter test data:
```json
{
  "full_name": "Test User",
  "email": "test@example.com",
  "password": "password123"
}
```
5. Click "Execute"

**Expected:** 200 response with user data

### 5. Seed Universities
Open: http://localhost:8000/api/universities/seed

**Expected Response:**
```json
{
  "message": "Universities seeded successfully"
}
```

## Frontend Verification

### 1. Check Frontend is Running
Open: http://localhost:3000

**Expected:** Landing page with:
- "StudyAbroad AI" logo
- Headline about study abroad
- "Get Started" and "Login" buttons
- Three feature cards

### 2. Test Signup Flow
1. Click "Get Started"
2. Fill signup form
3. Submit

**Expected:** Redirect to onboarding page

### 3. Test Onboarding
1. Complete Step 1 (Academic)
2. Complete Step 2 (Study Goals)
3. Complete Step 3 (Budget)
4. Complete Step 4 (Exams)
5. Click "Complete Onboarding"

**Expected:** Redirect to dashboard

### 4. Verify Dashboard
Check dashboard shows:
- Welcome message with your name
- Current stage
- Profile strength indicators
- Navigation menu

## Integration Testing

### Test 1: Complete User Journey
```
 Landing page loads
 Signup successful
 Onboarding completes
 Dashboard shows profile
 Can navigate to universities
 Can access AI counselor
```

### Test 2: AI Counselor
1. Go to AI Counselor page
2. Type: "What universities should I apply to?"
3. Submit

**Expected:** AI response based on your profile

### Test 3: University Discovery
1. Go to Universities page
2. View recommendations
3. Shortlist a university

**Expected:** University added to shortlist with category badge

## Troubleshooting Checklist

### Backend Issues

#### "Connection refused" error
```bash
# Check backend is running
# Should see: Uvicorn running on http://127.0.0.1:8000

# If not running:
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload
```

#### "Database connection error"
```bash
# Check PostgreSQL is running
# Windows: Check Services
# Mac: brew services list
# Linux: sudo service postgresql status

# Verify database exists
psql -U postgres -l | grep study_abroad_db

# Create if missing
createdb study_abroad_db
```

#### "Module not found" error
```bash
cd backend
pip install -r requirements.txt
```

#### "Gemini API error"
```bash
# Check .env file has GEMINI_API_KEY
cat .env | grep GEMINI_API_KEY

# Get free key at: https://makersuite.google.com/app/apikey
```

### Frontend Issues

#### "Cannot connect to API"
```bash
# Check .env.local file
cat .env.local

# Should contain:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Verify backend is running on port 8000
```

#### "Page not found" error
```bash
# Clear Next.js cache
rm -rf .next
npm run dev
```

#### "Module not found" error
```bash
cd frontend
npm install
```

#### Port 3000 already in use
```bash
# Use different port
npm run dev -- -p 3001
```

## Environment Variables Check

### Backend (.env)
```bash
cd backend
cat .env
```

**Should contain:**
- DATABASE_URL=postgresql://...
- SECRET_KEY=...
- GEMINI_API_KEY=...
- ALGORITHM=HS256
- ACCESS_TOKEN_EXPIRE_MINUTES=30

### Frontend (.env.local)
```bash
cd frontend
cat .env.local
```

**Should contain:**
- NEXT_PUBLIC_API_URL=http://localhost:8000/api

## API Endpoint Tests

### Using cURL

```bash
# Health Check
curl http://localhost:8000/health

# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test","email":"test@test.com","password":"pass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"pass123"}'

# Get Universities (requires auth token)
curl -X GET http://localhost:8000/api/universities/recommendations \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Database Verification

### Check Tables Created
```sql
-- Connect to database
psql -U postgres -d study_abroad_db

-- List tables
\dt

-- Should see:
-- users
-- user_profiles
-- universities
-- shortlisted_universities
-- todo_items
-- chat_messages

-- Check universities seeded
SELECT COUNT(*) FROM universities;
-- Should return: 10

-- Exit
\q
```

## Feature Checklist

### Core Features
- [ ] Landing page displays correctly
- [ ] Signup creates user account
- [ ] Login authenticates user
- [ ] Onboarding saves profile
- [ ] Dashboard shows data
- [ ] Profile strength calculated
- [ ] Universities load
- [ ] Shortlisting works
- [ ] AI counselor responds
- [ ] Tasks display
- [ ] Profile edits save

### AI Features
- [ ] Profile strength auto-calculated
- [ ] Universities categorized (Dream/Target/Safe)
- [ ] AI counselor provides responses
- [ ] Tasks auto-generated
- [ ] Acceptance chances calculated

### Flow Control
- [ ] Onboarding required before dashboard
- [ ] AI counselor locked until onboarding
- [ ] University locking changes stage
- [ ] Profile edits trigger recalculation

## Performance Check

### Backend Response Times
- API root: < 100ms
- Signup: < 500ms
- Dashboard: < 300ms
- AI counselor: < 3s (depends on Gemini)

### Frontend Load Times
- Landing page: < 1s
- Dashboard: < 2s
- Page navigation: < 500ms

## Success Criteria

 All pages load without errors
 Backend API returns valid responses
 Database operations work
 AI counselor provides responses
 Universities are seeded and visible
 User can complete full journey

## Next Steps

Once verification passes:

1. **Customize**: Add your own data
2. **Test**: Try different user scenarios
3. **Deploy**: Follow DEPLOYMENT.md
4. **Demo**: Prepare presentation

## Getting Help

If issues persist:

1. Check error messages in:
   - Browser console (F12)
   - Backend terminal
   - Frontend terminal

2. Review documentation:
   - README.md
   - QUICKSTART.md
   - Backend/Frontend README files

3. Verify environment variables

4. Check PostgreSQL logs

5. Test with fresh database:
```bash
dropdb study_abroad_db
createdb study_abroad_db
# Restart backend
```

---

**Verification Complete? Start Building! **
