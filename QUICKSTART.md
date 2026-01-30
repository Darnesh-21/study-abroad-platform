# Quick Start - Study Abroad Platform

##  Get Started in 5 Minutes

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+

### Step 1: Clone and Setup (1 minute)

```bash
cd study-abroad-platform
```

### Step 2: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Or Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env and add:
# - Database URL
# - Secret key
# - Gemini API key (get from https://makersuite.google.com/app/apikey)
```

### Step 3: Database Setup (30 seconds)

```bash
# Create PostgreSQL database
createdb study_abroad_db

# Or using psql:
# psql -U postgres
# CREATE DATABASE study_abroad_db;
```

### Step 4: Start Backend (30 seconds)

```bash
# Still in backend directory
uvicorn main:app --reload
```

Backend runs at: http://localhost:8000

### Step 5: Seed Universities (10 seconds)

Open browser: http://localhost:8000/api/universities/seed

### Step 6: Frontend Setup (1 minute)

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Create .env.local
copy .env.local.example .env.local

# Start frontend
npm run dev
```

Frontend runs at: http://localhost:3000

### Step 7: Test the Platform

1. Open http://localhost:3000
2. Click "Get Started" 
3. Create an account
4. Complete onboarding
5. Explore the dashboard!

##  What's Included

 Complete authentication system
 4-step onboarding wizard
 AI-powered counselor (Gemini)
 University matching algorithm
 Smart shortlisting (Dream/Target/Safe)
 University locking mechanism
 AI-generated to-do lists
 Profile strength assessment
 Real-time chat interface
 Responsive design
 PostgreSQL database

##  Project Structure

```
study-abroad-platform/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── models.py    # Database models
│   │   ├── schemas.py   # Pydantic schemas
│   │   └── ...
│   ├── main.py          # App entry point
│   └── requirements.txt
│
├── frontend/            # Next.js frontend
│   ├── app/            # Pages (App Router)
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── onboarding/
│   │   └── ...
│   ├── lib/            # Utilities
│   └── package.json
│
├── README.md
├── DEPLOYMENT.md
└── QUICKSTART.md
```

##  Important Files

### Backend
- `backend/.env` - Environment variables (DATABASE_URL, GEMINI_API_KEY, SECRET_KEY)
- `backend/main.py` - FastAPI application
- `backend/app/models.py` - Database schema
- `backend/app/api/counselor.py` - AI counselor logic

### Frontend
- `frontend/.env.local` - Frontend environment (NEXT_PUBLIC_API_URL)
- `frontend/app/page.tsx` - Landing page
- `frontend/app/dashboard/page.tsx` - Main dashboard
- `frontend/lib/api.ts` - API client

##  Testing

### Test Backend APIs
Visit: http://localhost:8000/docs (Swagger UI)

### Test Frontend Pages
- Landing: http://localhost:3000
- Signup: http://localhost:3000/auth/signup
- Login: http://localhost:3000/auth/login
- Dashboard: http://localhost:3000/dashboard (after login)

##  Sample Workflow

1. **Sign Up** → Create account with email/password
2. **Onboarding** → Complete 4-step profile setup
3. **Dashboard** → View profile strength and tasks
4. **Universities** → Browse and shortlist universities
5. **AI Counselor** → Chat for personalized guidance
6. **Lock Universities** → Lock favorites for application prep
7. **To-Do List** → Track AI-generated tasks

## ️ Common Issues

### Database Connection Error
```bash
# Ensure PostgreSQL is running
# Check DATABASE_URL in .env
```

### Gemini API Error
```bash
# Get free API key: https://makersuite.google.com/app/apikey
# Add to .env: GEMINI_API_KEY=your_key_here
```

### Port Already in Use
```bash
# Backend: Use different port
uvicorn main:app --reload --port 8001

# Frontend: Use different port
npm run dev -- -p 3001
```

### Module Not Found
```bash
# Backend: Reinstall dependencies
pip install -r requirements.txt

# Frontend: Reinstall dependencies
npm install
```

##  Documentation

- [README.md](README.md) - Full project documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment guide
- [backend/README.md](backend/README.md) - Backend setup details
- [frontend/README.md](frontend/README.md) - Frontend setup details

##  Key Features

### AI-Powered
- Profile strength auto-calculation
- University categorization (Dream/Target/Safe)
- Acceptance chance prediction
- AI-generated task lists
- Conversational counselor with context

### University Matching
- Budget-based filtering
- Country preferences
- Field alignment
- GPA/test score requirements
- Acceptance rate analysis

### User Journey
- Stage-based progression
- Mandatory onboarding gate
- University locking mechanism
- Application tracking
- Profile editing with recalculation

##  Next Steps

After getting it running:

1. **Customize**: Modify university data, add more fields
2. **Enhance AI**: Fine-tune Gemini prompts for better responses
3. **Add Features**: Voice chat, document upload, more filters
4. **Integrate APIs**: Real university databases, exam booking APIs
5. **Deploy**: Follow DEPLOYMENT.md for production

##  Pro Tips

1. Use the AI counselor to test different scenarios
2. The system auto-generates tasks based on profile
3. Profile edits trigger recalculation of everything
4. Universities are categorized based on your actual stats
5. Locked universities unlock application-specific guidance

##  Hackathon Checklist

- [x] Landing page with clear value proposition
- [x] Authentication (signup/login)
- [x] Mandatory onboarding flow
- [x] Dashboard with profile strength
- [x] AI counselor integration
- [x] University discovery and matching
- [x] Shortlisting with Dream/Target/Safe categories
- [x] University locking mechanism
- [x] AI-generated to-do lists
- [x] Profile management
- [x] Responsive design
- [x] PostgreSQL database
- [x] Clean code structure
- [x] Deployment ready

##  Support

For questions or issues:
1. Check documentation files
2. Review API docs at /docs
3. Check browser console for errors
4. Verify environment variables

---

**Happy Hacking! **

Built with ️ using FastAPI, Next.js, and Gemini AI
