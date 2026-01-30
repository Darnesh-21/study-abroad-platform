from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, onboarding, dashboard, counselor, universities, profile, todos
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Study Abroad Platform API",
    description="AI-powered study abroad planning platform",
    version="1.0.0"
)

# CORS middleware - Allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(onboarding.router, prefix="/api/onboarding", tags=["Onboarding"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(counselor.router, prefix="/api/counselor", tags=["AI Counselor"])
app.include_router(universities.router, prefix="/api/universities", tags=["Universities"])
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"])
app.include_router(todos.router, prefix="/api/todos", tags=["To-Do List"])

@app.get("/")
async def root():
    return {"message": "Study Abroad Platform API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
