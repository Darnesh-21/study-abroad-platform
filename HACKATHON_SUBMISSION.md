# Study Abroad Platform - Hackathon Submission

##  Project Overview

A comprehensive AI-powered platform that guides students through their entire study-abroad journey, from profile building to university applications.

##  Key Features Implemented

### 1. **Landing Page** 
- Clean, modern design
- Clear value proposition
- Product features showcase
- Call-to-action buttons

### 2. **Authentication System** 
- Email/password signup
- Secure login with JWT tokens
- Password hashing (bcrypt)
- Auto-redirect based on auth state

### 3. **Mandatory Onboarding** 
**4-Step Wizard:**
- **Step 1**: Academic Background (education, major, GPA)
- **Step 2**: Study Goals (degree, field, countries, intake year)
- **Step 3**: Budget & Funding (range, funding plan)
- **Step 4**: Exams & Readiness (IELTS/TOEFL, GRE/GMAT, SOP)

**Gates:**
- Dashboard locked until onboarding complete
- AI Counselor locked until onboarding complete
- Profile strength calculated upon completion

### 4. **Dashboard (Control Center)** 
**Answers Three Questions:**
- Where am I? → Current Stage indicator
- What should I do? → AI-generated to-do list
- How strong is my profile? → Strength assessment

**Features:**
- Profile summary card
- Profile strength visualization (Academic/Exams/Overall)
- Stage progression tracker
- Shortlisted universities count
- Pending tasks overview
- Quick action buttons

### 5. **AI Counselor (Gemini-Powered)** 
**Capabilities:**
- Context-aware conversations
- Profile analysis and recommendations
- University suggestions with reasoning
- Risk factor identification
- Personalized guidance
- Action execution (shortlist, tasks)

**Context Includes:**
- Complete user profile
- Shortlisted universities
- Current stage
- Pending tasks
- Conversation history

### 6. **University Discovery & Matching** 
**Smart Matching Algorithm:**
- Budget-based filtering
- Country preference alignment
- Field of study matching
- GPA/test score requirements
- Acceptance rate analysis

**Categorization (AI-Driven):**
- **Dream**: Reach schools (low acceptance chance)
- **Target**: Match schools (good fit)
- **Safe**: Safety schools (high acceptance chance)

**Sample Universities:**
- USA: MIT, Stanford, CMU, UC Berkeley
- UK: Oxford, Cambridge, Imperial College
- Canada: University of Toronto, UBC
- Germany: Technical University of Munich

### 7. **University Shortlisting** 
**Features:**
- Add to shortlist with category
- AI-generated fit analysis
- Risk factor identification
- Acceptance chance prediction
- Cost level assessment
- Remove from shortlist

### 8. **University Locking** 
**Critical Feature:**
- Lock universities to commit
- Unlocks application-specific guidance
- Changes user stage to "Preparing Applications"
- Warning on unlock
- Tracks lock timestamp

### 9. **AI-Powered To-Do System** 
**Auto-Generated Tasks:**
- Exam registration reminders
- SOP writing tasks
- Research activities
- Based on profile gaps
- Priority assignment
- Category tagging

**Manual Tasks:**
- User-created tasks
- Priority setting
- Due dates
- Completion tracking

### 10. **Profile Management** 
**Editable Fields:**
- All onboarding data
- Real-time updates
- Triggers recalculation:
  - Profile strength
  - University recommendations
  - Acceptance chances
  - Task list

### 11. **Profile Strength Assessment** 
**AI-Calculated:**
- **Academic Strength**: Based on GPA
  - Strong: GPA ≥ 3.5
  - Average: GPA 3.0-3.4
  - Weak: GPA < 3.0

- **Exam Strength**: Based on test completion
  - Strong: Both tests complete
  - Average: One test complete
  - Weak: No tests complete

- **Overall Strength**: Composite score

## ️ Technical Implementation

### Backend (FastAPI)
**Structure:**
```
backend/
├── main.py                    # FastAPI app
├── app/
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── database.py           # DB connection
│   ├── config.py             # Settings
│   ├── auth_utils.py         # JWT/password handling
│   └── api/
│       ├── auth.py           # Signup/login
│       ├── onboarding.py     # Profile setup
│       ├── dashboard.py      # Dashboard data
│       ├── profile.py        # Profile management
│       ├── universities.py   # University operations
│       ├── todos.py          # Task management
│       └── counselor.py      # AI chat
```

**Technologies:**
- FastAPI 0.109.0
- PostgreSQL (SQLAlchemy ORM)
- Google Gemini AI
- JWT authentication
- Bcrypt password hashing
- Pydantic validation

### Frontend (Next.js)
**Structure:**
```
frontend/
├── app/
│   ├── page.tsx              # Landing page
│   ├── layout.tsx            # Root layout
│   ├── auth/
│   │   ├── login/           # Login page
│   │   └── signup/          # Signup page
│   ├── onboarding/          # 4-step wizard
│   ├── dashboard/           # Main dashboard
│   ├── universities/        # Discovery page
│   ├── counselor/           # AI chat
│   └── profile/             # Profile edit
├── lib/
│   ├── api.ts               # API client
│   ├── store.ts             # Zustand state
│   └── types.ts             # TypeScript types
```

**Technologies:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Zustand (state management)
- Axios (HTTP client)

### Database Schema
**Key Tables:**
- `users` - User accounts
- `user_profiles` - Student profiles
- `universities` - University data
- `shortlisted_universities` - User shortlists with AI insights
- `todo_items` - Tasks (AI + manual)
- `chat_messages` - Counselor conversations

##  Core Flow Demonstration

### 1. User Journey
```
Landing Page
    ↓
Signup/Login
    ↓
Onboarding (4 steps) → Profile Created
    ↓
Dashboard → Profile Strength Calculated
    ↓
Discover Universities → AI Recommendations
    ↓
Shortlist Universities → AI Analysis
    ↓
Chat with AI Counselor → Personalized Guidance
    ↓
Lock Universities → Application Prep Begins
    ↓
Follow To-Do List → Complete Applications
```

### 2. AI Integration Points

**Profile Analysis:**
- Automatic strength calculation
- Gap identification
- Recommendation generation

**University Matching:**
- Dream/Target/Safe categorization
- Fit reason generation
- Risk factor identification
- Acceptance chance prediction

**Counselor Conversations:**
- Context-aware responses
- Profile-based recommendations
- Action execution
- Task generation

##  Unique Features

### 1. **Strict Flow Control**
- Onboarding gates dashboard access
- Stages unlock progressively
- Locking mechanism for commitment

### 2. **AI-Driven Everything**
- Profile strength auto-calculated
- Universities auto-categorized
- Tasks auto-generated
- Risks auto-identified

### 3. **Context-Aware AI**
- Knows complete profile
- Understands current stage
- Aware of shortlisted universities
- Remembers conversation history

### 4. **Real-Time Recalculation**
- Profile edits trigger updates
- University recommendations refresh
- Tasks adapt to changes
- Acceptance chances recalculate

##  Deployment Ready

### Production Features
- Environment variable configuration
- CORS setup for production
- Database migrations ready
- Build scripts configured
- Deployment guides included

### Deployment Options
- **Vercel** (Frontend) + **Render** (Backend)
- **Railway** (Full stack)
- **AWS/Azure/GCP** (Enterprise)

##  Scalability

### Current Architecture Supports:
- Horizontal scaling (stateless backend)
- Database connection pooling
- API rate limiting
- Caching opportunities
- CDN integration

### Future Enhancements:
- Redis caching
- Background job queue
- WebSocket for real-time chat
- Voice interface
- Document upload/storage

##  Hackathon Requirements Met

| Requirement | Status | Implementation |
|------------|--------|----------------|
| Landing Page |  | Clean design, clear CTA |
| Signup/Login |  | JWT auth, secure passwords |
| Mandatory Onboarding |  | 4-step wizard with gates |
| Dashboard |  | Profile, stage, tasks, strength |
| AI Counselor |  | Gemini integration, context-aware |
| University Shortlisting |  | Dream/Target/Safe with AI insights |
| University Locking |  | Commitment mechanism |
| Application Guidance |  | Task-based guidance system |
| Profile Management |  | Full CRUD with recalculation |
| Clean UI/UX |  | Tailwind CSS, responsive |
| Code Quality |  | Typed, structured, documented |
| Free APIs |  | Gemini (free tier) |

##  Innovation Points

### 1. **AI-First Approach**
Unlike traditional platforms, every feature is AI-enhanced:
- No manual categorization
- No static recommendations
- Dynamic, profile-aware guidance

### 2. **Commitment Mechanism**
University locking forces intentional decision-making and unlocks personalized prep.

### 3. **Context Persistence**
AI counselor maintains full context across sessions, providing truly personalized guidance.

### 4. **Stage-Based Journey**
Clear progression through defined stages with appropriate feature unlocking.

##  Documentation

### Included Guides
1. **README.md** - Complete project documentation
2. **QUICKSTART.md** - 5-minute setup guide
3. **DEPLOYMENT.md** - Production deployment
4. **backend/README.md** - Backend setup
5. **frontend/README.md** - Frontend setup

### Code Documentation
- Inline comments
- Function docstrings
- Type hints
- Clear naming conventions

##  Demo Flow

**Recommended Demo Script:**

1. **Start**: Show landing page, highlight features
2. **Signup**: Create account quickly
3. **Onboarding**: Complete 4 steps, show progress bar
4. **Dashboard**: Point out profile strength, stage, tasks
5. **Universities**: Filter, show Dream/Target/Safe badges
6. **Shortlist**: Add university, show AI insights
7. **AI Counselor**: Ask "What universities should I apply to?"
8. **Lock**: Lock a university, show stage change
9. **Tasks**: Show AI-generated vs manual tasks
10. **Profile Edit**: Change GPA, show recalculation

##  Competitive Advantages

1. **Complete Solution**: Not just discovery, entire journey
2. **AI-Powered**: True AI integration, not just chatbot
3. **Production Ready**: Deployable, scalable, documented
4. **User-Centric**: Clear flow, no confusion
5. **Free Tier**: Works with free APIs only

##  Deliverables

 Source code (Backend + Frontend)
 Database schema
 API documentation (Swagger at /docs)
 Setup guides
 Deployment guides
 README with complete instructions
 .env examples
 Sample data seeding
 Clean UI/UX

##  Success Metrics

**For Students:**
- Time to first recommendation: < 10 minutes
- Profile completion rate: 100% (gated)
- AI counselor engagement: High (contextual)
- University shortlisting: Easy (categorized)

**For Platform:**
- Code quality: High (typed, structured)
- Deployment: Simple (documented)
- Scalability: Ready (stateless)
- Cost: Low (free tier APIs)

---

##  Getting Started

See [QUICKSTART.md](QUICKSTART.md) for 5-minute setup guide.

##  Contact

For questions or support, please refer to the documentation files or open an issue in the repository.

---

**Built with ️ for the Study Abroad Hackathon**

**Tech Stack:** FastAPI • Next.js • PostgreSQL • Gemini AI • TypeScript • Tailwind CSS

**Status:**  Production Ready
