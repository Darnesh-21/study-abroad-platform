# Study Abroad Platform - AI-Powered Guidance

A comprehensive platform to help students plan their study-abroad journey with AI-powered counseling, university recommendations, and application tracking.

##  Project Overview

This platform provides end-to-end support for students planning to study abroad:

- **AI Counselor**: Get personalized guidance using Google's Gemini AI
- **Smart University Matching**: Find universities categorized as Dream, Target, and Safe
- **Profile Management**: Track academic strength and application readiness
- **Application Tracking**: AI-generated to-do lists and progress monitoring
- **University Locking**: Lock universities to get specific application guidance

## ️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **AI**: Google Gemini API
- **Authentication**: JWT tokens
- **ORM**: SQLAlchemy

### Frontend (Next.js)
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **API Client**: Axios

##  Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Google Gemini API key (free tier available)

##  Quick Start

### 1. Clone the Repository

```bash
cd study-abroad-platform
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env and add your credentials
```

#### Environment Variables (.env)

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/study_abroad_db
SECRET_KEY=your-secret-key-here-change-in-production
GEMINI_API_KEY=your-gemini-api-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Get Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key (free tier available)
3. Copy the key to your .env file

#### Database Setup

```bash
# Install PostgreSQL and create database
createdb study_abroad_db

# Or using psql:
psql -U postgres
CREATE DATABASE study_abroad_db;
\q

# Run the application (it will create tables automatically)
uvicorn main:app --reload
```

Server will run at: http://localhost:8000

#### Seed Universities

Open your browser and navigate to:
```
http://localhost:8000/api/universities/seed
```

This will populate the database with sample universities.

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
copy .env.local.example .env.local
# Edit .env.local if needed (default should work)

# Run development server
npm run dev
```

Frontend will run at: http://localhost:3000

##  Application Flow

### 1. Landing Page
- Product introduction
- CTA buttons for signup/login

### 2. Authentication
- Signup with email/password
- Login with existing credentials

### 3. Onboarding (Mandatory)
Four-step process:
1. **Academic Background**: Education level, major, GPA
2. **Study Goals**: Intended degree, field, countries
3. **Budget & Funding**: Budget range, funding plan
4. **Exams & Readiness**: IELTS/TOEFL, GRE/GMAT, SOP status

### 4. Dashboard
Shows:
- Current stage in the journey
- Profile strength (Academic, Exams, Overall)
- Shortlisted universities
- AI-generated to-do list
- Quick actions

### 5. University Discovery
- AI-recommended universities based on profile
- Filter by country, field, budget
- Categories: Dream, Target, Safe
- Detailed fit analysis and risk factors

### 6. University Shortlisting & Locking
- Shortlist universities of interest
- Lock universities to unlock application guidance
- View acceptance chances and cost levels

### 7. AI Counselor
- Chat with Gemini-powered AI counselor
- Get personalized recommendations
- Ask questions about the process
- Context-aware responses based on profile

### 8. Profile Management
- Edit profile information
- Updates trigger:
  - Recalculation of university recommendations
  - Task list updates
  - Acceptance chance updates

##  Key Features

### AI-Powered Features
- **Profile Strength Calculation**: Automatic assessment of academic and exam readiness
- **University Categorization**: AI categorizes universities as Dream/Target/Safe
- **Acceptance Chance Prediction**: Estimates likelihood based on profile
- **AI-Generated Tasks**: Automatic to-do list creation
- **Conversational Counselor**: Context-aware AI guidance

### University Matching
- Budget-based filtering
- Country preferences
- Field of study alignment
- GPA and test score requirements
- Acceptance rate consideration

### Application Tracking
- Stage-based progression
- Priority-based task management
- AI vs manual task distinction
- Completion tracking

## ️ Database Schema

### Main Tables
- **users**: User accounts
- **user_profiles**: Student profiles and preferences
- **universities**: University data
- **shortlisted_universities**: User's shortlisted universities with AI insights
- **todo_items**: Tasks and to-do items
- **chat_messages**: AI counselor conversation history

##  API Endpoints

### Authentication
- `POST /api/auth/signup` - Create account
- `POST /api/auth/login` - Login

### Onboarding
- `POST /api/onboarding/complete` - Complete onboarding
- `GET /api/onboarding/status` - Get onboarding status

### Dashboard
- `GET /api/dashboard` - Get dashboard data

### Profile
- `GET /api/profile` - Get profile
- `PUT /api/profile` - Update profile

### Universities
- `GET /api/universities/recommendations` - Get recommended universities
- `POST /api/universities/shortlist` - Shortlist university
- `GET /api/universities/shortlisted` - Get shortlisted universities
- `POST /api/universities/lock/{id}` - Lock university
- `POST /api/universities/unlock/{id}` - Unlock university

### To-Dos
- `GET /api/todos` - Get to-do list
- `POST /api/todos` - Create task
- `PATCH /api/todos/{id}` - Update task
- `DELETE /api/todos/{id}` - Delete task

### AI Counselor
- `POST /api/counselor/chat` - Chat with AI
- `GET /api/counselor/history` - Get chat history

##  University Data

The platform includes sample data for universities from:
- USA (MIT, Stanford, CMU, UC Berkeley)
- UK (Oxford, Cambridge, Imperial College)
- Canada (University of Toronto, UBC)
- Germany (TUM)

**Note**: For production, integrate with real university APIs like:
- Universities API: https://github.com/Hipo/university-domains-list
- World Universities API
- Country-specific education databases

##  AI Integration

The platform uses Google's Gemini AI for:
- Conversational counseling
- University recommendations
- Profile strength assessment
- Risk factor identification

### Gemini Prompt Engineering

The system provides the AI with:
- Complete user profile context
- Shortlisted universities
- Current stage and pending tasks
- Conversation history

This enables personalized, context-aware responses.

##  Deployment

### Backend Deployment (Recommended: Render/Railway)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment (Recommended: Vercel)

```bash
# Build for production
npm run build

# Start production server
npm start
```

### Environment Variables for Production
- Update `DATABASE_URL` with production database
- Change `SECRET_KEY` to a strong random value
- Update `NEXT_PUBLIC_API_URL` to production API URL
- Ensure `GEMINI_API_KEY` is set

##  Database Migration (Optional)

For production, use Alembic for database migrations:

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

##  Security Considerations

- JWT tokens expire after 30 minutes
- Passwords are hashed using bcrypt
- CORS is configured for frontend origin
- Environment variables for sensitive data
- Input validation on all endpoints

##  Code Quality

- Type hints in Python code
- TypeScript for type safety in frontend
- Pydantic models for data validation
- React hooks for state management
- Clean component architecture

##  Troubleshooting

### Database Connection Error
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Ensure database exists

### Gemini API Error
- Verify API key is correct
- Check API quota/limits
- Ensure internet connection

### Frontend Not Loading
- Check API_URL in .env.local
- Verify backend is running
- Check browser console for errors

##  License

This project is for educational/hackathon purposes.

##  Acknowledgments

- Google Gemini API for AI capabilities
- FastAPI for excellent API framework
- Next.js for modern React development
- Tailwind CSS for styling

##  Support

For issues or questions, please open an issue in the repository.

---

**Happy Coding! **
