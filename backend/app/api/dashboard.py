from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, UserProfile, TodoItem, ShortlistedUniversity, UniversityDocument
from app.schemas import DashboardResponse, UserResponse, ProfileResponse, TodoResponse, ShortlistedUniversityResponse, CommittedUniversityData, UniversityDocumentResponse
from app.auth_utils import get_current_user

router = APIRouter()

@router.get("/", response_model=DashboardResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get user profile
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Get all incomplete todos (not limited - we need accurate count)
    todos = db.query(TodoItem).filter(
        TodoItem.user_id == current_user.id,
        TodoItem.is_completed == False
    ).order_by(TodoItem.created_at.desc()).all()
    
    # Get shortlisted universities
    shortlisted = db.query(ShortlistedUniversity).filter(
        ShortlistedUniversity.user_id == current_user.id
    ).all()
    
    # Get locked universities with their documents and tasks
    locked_universities = db.query(ShortlistedUniversity).filter(
        ShortlistedUniversity.user_id == current_user.id,
        ShortlistedUniversity.is_locked == True
    ).all()
    
    # Convert all ORM objects to Pydantic models for response
    user_response = UserResponse.model_validate(current_user)
    profile_response = ProfileResponse.model_validate(profile)
    todos_response = [TodoResponse.model_validate(todo) for todo in todos]
    shortlisted_response = [ShortlistedUniversityResponse.model_validate(uni) for uni in shortlisted]
    
    # Build committed universities data with tasks and documents
    committed_unis = []
    for locked_uni in locked_universities:
        # Get tasks for this specific university by matching university name in task title
        university_name = locked_uni.university.name
        uni_tasks = db.query(TodoItem).filter(
            TodoItem.user_id == current_user.id,
            TodoItem.is_completed == False,
            TodoItem.title.contains(university_name)
        ).all()
        
        # Get documents for this university
        documents = db.query(UniversityDocument).filter(
            UniversityDocument.user_id == current_user.id,
            UniversityDocument.shortlisted_university_id == locked_uni.id
        ).all()
        
        # Convert ORM objects to Pydantic models
        locked_uni_response = ShortlistedUniversityResponse.model_validate(locked_uni)
        tasks_response = [TodoResponse.model_validate(task) for task in uni_tasks]
        documents_response = [UniversityDocumentResponse.model_validate(doc) for doc in documents]
        
        committed_unis.append(CommittedUniversityData(
            shortlisted_university=locked_uni_response,
            tasks=tasks_response,
            documents=documents_response
        ))
    
    # Count locked universities
    locked_count = len(locked_universities)
    
    return DashboardResponse(
        user=user_response,
        profile=profile_response,
        todos=todos_response,
        shortlisted_universities=shortlisted_response,
        locked_universities_count=locked_count,
        committed_universities=committed_unis
    )
