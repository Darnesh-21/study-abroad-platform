from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from app.database import get_db
from app.models import User, UserProfile, UserStage, ProfileStrength, TodoItem
from app.schemas import OnboardingData, ProfileResponse
from app.auth_utils import get_current_user

router = APIRouter()

def calculate_profile_strength(profile: UserProfile) -> dict:
    """Calculate profile strength based on various factors"""
    
    # Academic strength
    if profile.gpa_percentage:
        if profile.gpa_percentage >= 3.5:
            academic_strength = ProfileStrength.STRONG
        elif profile.gpa_percentage >= 3.0:
            academic_strength = ProfileStrength.AVERAGE
        else:
            academic_strength = ProfileStrength.WEAK
    else:
        academic_strength = ProfileStrength.AVERAGE
    
    # Exam strength
    exam_completed = 0
    if profile.ielts_toefl_status.value == "completed":
        exam_completed += 1
    if profile.gre_gmat_status.value == "completed":
        exam_completed += 1
    
    if exam_completed == 2:
        exam_strength = ProfileStrength.STRONG
    elif exam_completed == 1:
        exam_strength = ProfileStrength.AVERAGE
    else:
        exam_strength = ProfileStrength.WEAK
    
    # Overall strength
    strengths = [academic_strength, exam_strength]
    strong_count = sum(1 for s in strengths if s == ProfileStrength.STRONG)
    weak_count = sum(1 for s in strengths if s == ProfileStrength.WEAK)
    
    if strong_count >= 2:
        overall_strength = ProfileStrength.STRONG
    elif weak_count >= 2:
        overall_strength = ProfileStrength.WEAK
    else:
        overall_strength = ProfileStrength.AVERAGE
    
    return {
        "academic_strength": academic_strength,
        "exam_strength": exam_strength,
        "overall_strength": overall_strength
    }

def generate_initial_todos(user_id: int, profile: UserProfile, db: Session):
    """Generate initial AI-powered to-do items based on profile"""
    todos = []
    
    # Exam-related todos
    if profile.ielts_toefl_status.value == "not_started":
        todos.append(TodoItem(
            user_id=user_id,
            title="Register for IELTS/TOEFL",
            description="Book your English proficiency test",
            priority="High",
            category="Exams",
            ai_generated=True
        ))
    
    if profile.gre_gmat_status.value == "not_started":
        todos.append(TodoItem(
            user_id=user_id,
            title="Start GRE/GMAT Preparation",
            description="Begin preparing for your standardized test",
            priority="High",
            category="Exams",
            ai_generated=True
        ))
    
    # SOP-related todos
    if profile.sop_status.value == "not_started":
        todos.append(TodoItem(
            user_id=user_id,
            title="Start SOP Draft",
            description="Begin writing your Statement of Purpose",
            priority="Medium",
            category="Documents",
            ai_generated=True
        ))
    
    # Research todos
    todos.append(TodoItem(
        user_id=user_id,
        title="Research Universities",
        description=f"Explore universities in {profile.preferred_countries}",
        priority="High",
        category="Research",
        ai_generated=True
    ))
    
    for todo in todos:
        db.add(todo)

@router.post("/complete", response_model=ProfileResponse)
async def complete_onboarding(
    onboarding_data: OnboardingData,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Update profile with onboarding data
    profile.current_education_level = onboarding_data.current_education_level
    profile.degree_major = onboarding_data.degree_major
    profile.graduation_year = onboarding_data.graduation_year
    profile.gpa_percentage = onboarding_data.gpa_percentage
    profile.intended_degree = onboarding_data.intended_degree
    profile.field_of_study = onboarding_data.field_of_study
    profile.target_intake_year = onboarding_data.target_intake_year
    profile.preferred_countries = json.dumps(onboarding_data.preferred_countries)
    profile.budget_min = onboarding_data.budget_min
    profile.budget_max = onboarding_data.budget_max
    profile.funding_plan = onboarding_data.funding_plan
    profile.ielts_toefl_status = onboarding_data.ielts_toefl_status
    profile.ielts_toefl_score = onboarding_data.ielts_toefl_score
    profile.gre_gmat_status = onboarding_data.gre_gmat_status
    profile.gre_gmat_score = onboarding_data.gre_gmat_score
    profile.sop_status = onboarding_data.sop_status
    
    # Calculate profile strength
    strengths = calculate_profile_strength(profile)
    profile.academic_strength = strengths["academic_strength"]
    profile.exam_strength = strengths["exam_strength"]
    profile.overall_strength = strengths["overall_strength"]
    
    # Mark onboarding as completed and move to next stage
    profile.onboarding_completed = True
    profile.current_stage = UserStage.DISCOVERING_UNIVERSITIES
    
    db.commit()
    
    # Generate initial to-do items
    generate_initial_todos(current_user.id, profile, db)
    db.commit()
    
    db.refresh(profile)
    return profile

@router.get("/status", response_model=ProfileResponse)
async def get_onboarding_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile
