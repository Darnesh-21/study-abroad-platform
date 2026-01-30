from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from app.database import get_db
from app.models import User, UserProfile, ProfileStrength, UserStage
from app.schemas import ProfileResponse, ProfileUpdate
from app.auth_utils import get_current_user

router = APIRouter()

def recalculate_profile_strength(profile: UserProfile) -> dict:
    """Recalculate profile strength when profile is updated"""
    
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
    if profile.ielts_toefl_status and profile.ielts_toefl_status.value == "completed":
        exam_completed += 1
    if profile.gre_gmat_status and profile.gre_gmat_status.value == "completed":
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

@router.get("/", response_model=ProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile

@router.put("/", response_model=ProfileResponse)
async def update_profile(
    profile_update: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Update fields
    update_data = profile_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == "preferred_countries" and value is not None:
            setattr(profile, field, json.dumps(value))
        elif value is not None:
            setattr(profile, field, value)
    
    # Mark profile as completed if it wasn't already
    if not profile.onboarding_completed:
        profile.onboarding_completed = True
        profile.current_stage = UserStage.DISCOVERING_UNIVERSITIES
    
    # Recalculate profile strength
    strengths = recalculate_profile_strength(profile)
    profile.academic_strength = strengths["academic_strength"]
    profile.exam_strength = strengths["exam_strength"]
    profile.overall_strength = strengths["overall_strength"]
    
    db.commit()
    db.refresh(profile)
    
    return profile
