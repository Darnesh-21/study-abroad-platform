from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import datetime, timedelta
from app.database import get_db
from app.models import User, UserProfile, University, ShortlistedUniversity, UniversityCategory, UserStage, TodoItem, UniversityDocument, DocumentType, DocumentStatus
from app.schemas import UniversityResponse, ShortlistedUniversityCreate, ShortlistedUniversityResponse
from app.auth_utils import get_current_user
from app.services.university_service import import_universities_from_api, search_universities_api

router = APIRouter()

def generate_application_tasks(db: Session, user_id: int, university: University, profile: UserProfile):
    """Generate application-specific tasks when a university is locked"""
    
    tasks = [
        {
            "title": f"Research {university.name} application deadlines",
            "description": f"Find and note all deadlines for {university.name} including application, financial aid, and scholarship deadlines.",
            "priority": "High",
            "category": "Research",
            "due_days": 3
        },
        {
            "title": f"Tailor SOP for {university.name}",
            "description": f"Customize your Statement of Purpose specifically for {university.name}, highlighting why this university aligns with your goals.",
            "priority": "High",
            "category": "Documents",
            "due_days": 14
        },
        {
            "title": f"Review {university.name} specific requirements",
            "description": f"Check program-specific requirements for {university.name} including transcripts, test scores, and additional documents.",
            "priority": "High",
            "category": "Requirements",
            "due_days": 7
        },
        {
            "title": f"Prepare application budget for {university.name}",
            "description": f"Calculate total costs including application fee, tuition, living expenses, and travel for {university.name}.",
            "priority": "Medium",
            "category": "Finance",
            "due_days": 10
        },
        {
            "title": f"Research scholarships at {university.name}",
            "description": f"Find scholarship opportunities specific to {university.name} and prepare required documents.",
            "priority": "Medium" if profile.funding_plan.value == "SCHOLARSHIP_DEPENDENT" else "Low",
            "category": "Finance",
            "due_days": 14
        },
        {
            "title": f"Get recommendation letters for {university.name}",
            "description": f"Request and collect recommendation letters tailored for {university.name}'s requirements.",
            "priority": "High",
            "category": "Documents",
            "due_days": 21
        },
        {
            "title": f"Verify test score requirements for {university.name}",
            "description": f"Ensure your IELTS/TOEFL and GRE/GMAT scores meet {university.name}'s minimum requirements.",
            "priority": "High",
            "category": "Exams",
            "due_days": 5
        }
    ]
    
    # Add tasks to database
    for task_data in tasks:
        # Check if similar task already exists
        existing = db.query(TodoItem).filter(
            TodoItem.user_id == user_id,
            TodoItem.title == task_data["title"],
            TodoItem.is_completed == False
        ).first()
        
        if not existing:
            due_date = datetime.utcnow() + timedelta(days=task_data["due_days"])
            todo = TodoItem(
                user_id=user_id,
                title=task_data["title"],
                description=task_data["description"],
                priority=task_data["priority"],
                category=task_data["category"],
                due_date=due_date,
                ai_generated=True
            )
            db.add(todo)
    
    # Commit tasks immediately
    db.flush()

def initialize_required_documents(db: Session, user_id: int, shortlisted_university_id: int):
    """Initialize required documents for a locked university"""
    
    documents = [
        {
            "type": DocumentType.SOP,
            "status": DocumentStatus.DRAFTING,
            "due_days": 14
        },
        {
            "type": DocumentType.RECOMMENDATION_LETTER,
            "status": DocumentStatus.PENDING,
            "due_days": 21
        },
        {
            "type": DocumentType.RESUME,
            "status": DocumentStatus.READY,
            "due_days": None
        },
        {
            "type": DocumentType.TRANSCRIPTS,
            "status": DocumentStatus.READY,
            "due_days": None
        }
    ]
    
    for doc_data in documents:
        # Check if document already exists
        existing = db.query(UniversityDocument).filter(
            UniversityDocument.user_id == user_id,
            UniversityDocument.shortlisted_university_id == shortlisted_university_id,
            UniversityDocument.document_type == doc_data["type"]
        ).first()
        
        if not existing:
            due_date = None
            if doc_data["due_days"]:
                due_date = datetime.utcnow() + timedelta(days=doc_data["due_days"])
            
            doc = UniversityDocument(
                user_id=user_id,
                shortlisted_university_id=shortlisted_university_id,
                document_type=doc_data["type"],
                status=doc_data["status"],
                due_date=due_date
            )
            db.add(doc)
    
    db.flush()

def seed_universities(db: Session):
    """Seed database with sample universities"""
    if db.query(University).count() > 0:
        return  # Already seeded
    
    universities_data = [
        # USA Universities
        {
            "name": "Massachusetts Institute of Technology",
            "country": "USA",
            "city": "Cambridge",
            "ranking": 1,
            "acceptance_rate": 7.3,
            "tuition_fee_min": 53000,
            "tuition_fee_max": 55000,
            "fields_offered": json.dumps(["Computer Science", "Engineering", "Business", "Data Science"]),
            "programs": json.dumps(["Master's in CS", "MBA", "MS in AI", "PhD in Engineering"]),
            "requirements": json.dumps({"ielts": 7.0, "gre": 320, "gpa": 3.5}),
            "description": "Top-ranked technology and research university",
            "website_url": "https://www.mit.edu"
        },
        {
            "name": "Stanford University",
            "country": "USA",
            "city": "Stanford",
            "ranking": 3,
            "acceptance_rate": 4.8,
            "tuition_fee_min": 52000,
            "tuition_fee_max": 54000,
            "fields_offered": json.dumps(["Computer Science", "Business", "Engineering", "Data Science"]),
            "programs": json.dumps(["MS in CS", "MBA", "MS in Data Science"]),
            "requirements": json.dumps({"ielts": 7.0, "gre": 325, "gpa": 3.7}),
            "description": "Premier university for innovation and entrepreneurship",
            "website_url": "https://www.stanford.edu"
        },
        {
            "name": "Carnegie Mellon University",
            "country": "USA",
            "city": "Pittsburgh",
            "ranking": 25,
            "acceptance_rate": 17.0,
            "tuition_fee_min": 48000,
            "tuition_fee_max": 50000,
            "fields_offered": json.dumps(["Computer Science", "Robotics", "AI", "Engineering"]),
            "programs": json.dumps(["MS in CS", "MS in AI", "MS in Robotics"]),
            "requirements": json.dumps({"ielts": 6.5, "gre": 315, "gpa": 3.3}),
            "description": "Leading university in computer science and AI",
            "website_url": "https://www.cmu.edu"
        },
        {
            "name": "University of California, Berkeley",
            "country": "USA",
            "city": "Berkeley",
            "ranking": 27,
            "acceptance_rate": 16.8,
            "tuition_fee_min": 45000,
            "tuition_fee_max": 47000,
            "fields_offered": json.dumps(["Computer Science", "Business", "Engineering", "Data Science"]),
            "programs": json.dumps(["MS in CS", "MBA", "MS in Data Science"]),
            "requirements": json.dumps({"ielts": 6.5, "gre": 310, "gpa": 3.2}),
            "description": "Public research university with strong programs",
            "website_url": "https://www.berkeley.edu"
        },
        # UK Universities
        {
            "name": "University of Oxford",
            "country": "UK",
            "city": "Oxford",
            "ranking": 4,
            "acceptance_rate": 17.5,
            "tuition_fee_min": 30000,
            "tuition_fee_max": 35000,
            "fields_offered": json.dumps(["Computer Science", "Business", "Engineering", "Law"]),
            "programs": json.dumps(["MSc in CS", "MBA", "MSc in Data Science"]),
            "requirements": json.dumps({"ielts": 7.5, "gre": 320, "gpa": 3.6}),
            "description": "Oldest university in the English-speaking world",
            "website_url": "https://www.ox.ac.uk"
        },
        {
            "name": "University of Cambridge",
            "country": "UK",
            "city": "Cambridge",
            "ranking": 5,
            "acceptance_rate": 21.0,
            "tuition_fee_min": 32000,
            "tuition_fee_max": 36000,
            "fields_offered": json.dumps(["Computer Science", "Engineering", "Business", "Mathematics"]),
            "programs": json.dumps(["MPhil in CS", "MBA", "MPhil in Engineering"]),
            "requirements": json.dumps({"ielts": 7.5, "gre": 320, "gpa": 3.6}),
            "description": "Historic university with world-class research",
            "website_url": "https://www.cam.ac.uk"
        },
        {
            "name": "Imperial College London",
            "country": "UK",
            "city": "London",
            "ranking": 8,
            "acceptance_rate": 14.3,
            "tuition_fee_min": 28000,
            "tuition_fee_max": 33000,
            "fields_offered": json.dumps(["Computer Science", "Engineering", "Business", "Medicine"]),
            "programs": json.dumps(["MSc in CS", "MSc in AI", "MSc in Data Science"]),
            "requirements": json.dumps({"ielts": 7.0, "gre": 315, "gpa": 3.4}),
            "description": "Science, engineering, and medicine focused university",
            "website_url": "https://www.imperial.ac.uk"
        },
        # Canada Universities
        {
            "name": "University of Toronto",
            "country": "Canada",
            "city": "Toronto",
            "ranking": 34,
            "acceptance_rate": 43.0,
            "tuition_fee_min": 25000,
            "tuition_fee_max": 30000,
            "fields_offered": json.dumps(["Computer Science", "Business", "Engineering", "Data Science"]),
            "programs": json.dumps(["MCS", "MBA", "MEng in CS"]),
            "requirements": json.dumps({"ielts": 6.5, "gre": 310, "gpa": 3.0}),
            "description": "Canada's top university with diverse programs",
            "website_url": "https://www.utoronto.ca"
        },
        {
            "name": "University of British Columbia",
            "country": "Canada",
            "city": "Vancouver",
            "ranking": 47,
            "acceptance_rate": 52.0,
            "tuition_fee_min": 22000,
            "tuition_fee_max": 28000,
            "fields_offered": json.dumps(["Computer Science", "Business", "Engineering"]),
            "programs": json.dumps(["MSc in CS", "MBA", "MEng"]),
            "requirements": json.dumps({"ielts": 6.5, "gre": 305, "gpa": 3.0}),
            "description": "Beautiful campus with strong research programs",
            "website_url": "https://www.ubc.ca"
        },
        # Germany Universities
        {
            "name": "Technical University of Munich",
            "country": "Germany",
            "city": "Munich",
            "ranking": 55,
            "acceptance_rate": 8.0,
            "tuition_fee_min": 0,
            "tuition_fee_max": 3000,
            "fields_offered": json.dumps(["Computer Science", "Engineering", "Business", "Robotics"]),
            "programs": json.dumps(["MSc in Informatics", "MSc in Robotics", "MBA"]),
            "requirements": json.dumps({"ielts": 6.5, "gre": 0, "gpa": 3.0}),
            "description": "Top technical university in Germany with low fees",
            "website_url": "https://www.tum.de"
        },
    ]
    
    for uni_data in universities_data:
        university = University(**uni_data)
        db.add(university)
    
    db.commit()

def categorize_university(profile: UserProfile, university: University) -> str:
    """Categorize university as Dream, Target, or Safe based on profile"""
    
    requirements = json.loads(university.requirements)
    user_gpa = profile.gpa_percentage or 3.0
    user_gre = profile.gre_gmat_score or 300
    
    required_gpa = requirements.get("gpa", 3.0)
    required_gre = requirements.get("gre", 300)
    
    # Calculate fit score
    gpa_diff = user_gpa - required_gpa
    gre_diff = user_gre - required_gre
    
    if university.acceptance_rate < 10 or gpa_diff < -0.2 or gre_diff < -10:
        return "dream"
    elif gpa_diff > 0.3 or gre_diff > 20:
        return "safe"
    else:
        return "target"

def calculate_acceptance_chance(profile: UserProfile, university: University) -> str:
    """Calculate acceptance chance"""
    
    requirements = json.loads(university.requirements)
    user_gpa = profile.gpa_percentage or 3.0
    user_gre = profile.gre_gmat_score or 300
    
    required_gpa = requirements.get("gpa", 3.0)
    required_gre = requirements.get("gre", 300)
    
    meets_requirements = user_gpa >= required_gpa and user_gre >= required_gre
    
    if university.acceptance_rate < 10:
        return "Low" if not meets_requirements else "Medium"
    elif university.acceptance_rate < 30:
        return "Medium" if not meets_requirements else "High"
    else:
        return "High"

def calculate_cost_level(profile: UserProfile, university: University) -> str:
    """Calculate cost level relative to budget"""
    
    avg_fee = (university.tuition_fee_min + university.tuition_fee_max) / 2
    
    if avg_fee > profile.budget_max:
        return "High"
    elif avg_fee < profile.budget_min:
        return "Low"
    else:
        return "Medium"

@router.get("/seed")
async def seed_universities_route(db: Session = Depends(get_db)):
    """Seed universities - for development only"""
    seed_universities(db)
    return {"message": "Sample universities seeded successfully"}

@router.get("/search", response_model=List[UniversityResponse])
async def search_universities(
    country: Optional[str] = None,
    name: Optional[str] = None,
    min_ranking: Optional[int] = None,
    max_ranking: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search all universities in database"""
    query = db.query(University)
    
    if country:
        query = query.filter(University.country == country)
    if name:
        query = query.filter(University.name.ilike(f"%{name}%"))
    if min_ranking:
        query = query.filter(University.ranking >= min_ranking)
    if max_ranking:
        query = query.filter(University.ranking <= max_ranking)
    
    universities = query.all()
    return universities

@router.get("/import-real")
async def import_real_universities_get(db: Session = Depends(get_db)):
    """Import real universities from Hipolabs API (GET method for browser)"""
    # Use standardized country names that match profile options
    countries = ["USA", "UK", "Canada", "Germany", "Australia", "Netherlands", "France", "Sweden"]
    
    try:
        count = await import_universities_from_api(db, countries, limit_per_country=50)
        return {
            "message": f"Successfully imported {count} real universities",
            "countries": countries,
            "count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import universities: {str(e)}")

@router.post("/import-real")
async def import_real_universities_post(
    db: Session = Depends(get_db),
    countries: List[str] = None
):
    """Import real universities from Hipolabs API (POST method with custom countries)"""
    if not countries:
        countries = ["United States", "United Kingdom", "Canada", "Germany", "Australia"]
    
    try:
        count = await import_universities_from_api(db, countries, limit_per_country=30)
        return {
            "message": f"Successfully imported {count} real universities",
            "countries": countries,
            "count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import universities: {str(e)}")

@router.get("/search-api")
async def search_from_api(
    country: Optional[str] = None,
    name: Optional[str] = None
):
    """Search universities directly from external API (no database)"""
    try:
        results = await search_universities_api(country=country, name=name)
        return {
            "count": len(results),
            "universities": results[:50]  # Limit to 50 results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search universities: {str(e)}")

@router.get("/recommendations", response_model=List[UniversityResponse])
async def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    country: Optional[str] = None,
    field: Optional[str] = None
):
    # Check if onboarding is completed
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile or not profile.onboarding_completed:
        raise HTTPException(status_code=400, detail="Please complete onboarding first")
    
    # Build query
    query = db.query(University)
    
    # Filter by preferred countries
    if profile.preferred_countries:
        countries = json.loads(profile.preferred_countries)
        query = query.filter(University.country.in_(countries))
    
    # Filter by country if provided
    if country:
        query = query.filter(University.country == country)
    
    # Filter by field if provided
    if field:
        query = query.filter(University.fields_offered.contains(field))
    
    # Filter by budget
    query = query.filter(
        University.tuition_fee_min <= profile.budget_max * 1.2  # 20% flexibility
    )
    
    universities = query.all()
    
    return universities

@router.post("/shortlist", response_model=ShortlistedUniversityResponse)
async def shortlist_university(
    shortlist_data: ShortlistedUniversityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if already shortlisted
    existing = db.query(ShortlistedUniversity).filter(
        ShortlistedUniversity.user_id == current_user.id,
        ShortlistedUniversity.university_id == shortlist_data.university_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="University already shortlisted")
    
    # Get university and profile
    university = db.query(University).filter(University.id == shortlist_data.university_id).first()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    # Generate AI insights
    category = categorize_university(profile, university)
    acceptance_chance = calculate_acceptance_chance(profile, university)
    cost_level = calculate_cost_level(profile, university)
    
    fit_reason = f"This university matches your {profile.field_of_study} interests and is located in {university.country}. "
    fit_reason += f"Your academic profile is well-suited for this {category} university."
    
    risk_factors = ""
    if acceptance_chance == "Low":
        risk_factors += "Highly competitive admission. "
    if cost_level == "High":
        risk_factors += "Tuition exceeds your budget range. "
    if not risk_factors:
        risk_factors = "No major risks identified."
    
    # Create shortlisted university
    shortlisted = ShortlistedUniversity(
        user_id=current_user.id,
        university_id=shortlist_data.university_id,
        category=UniversityCategory[shortlist_data.category.upper()],
        fit_reason=fit_reason,
        risk_factors=risk_factors,
        acceptance_chance=acceptance_chance,
        cost_level=cost_level
    )
    
    db.add(shortlisted)
    db.commit()
    db.refresh(shortlisted)
    
    # Update user stage progression
    # If this is their first shortlist, move to FINALIZING_UNIVERSITIES stage
    shortlist_count = db.query(ShortlistedUniversity).filter(
        ShortlistedUniversity.user_id == current_user.id
    ).count()
    
    if shortlist_count == 1 and profile.current_stage == UserStage.DISCOVERING_UNIVERSITIES:
        profile.current_stage = UserStage.FINALIZING_UNIVERSITIES
        db.commit()
    
    return shortlisted

@router.get("/shortlisted", response_model=List[ShortlistedUniversityResponse])
async def get_shortlisted(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shortlisted = db.query(ShortlistedUniversity).filter(
        ShortlistedUniversity.user_id == current_user.id
    ).all()
    
    return shortlisted

@router.post("/lock/{university_id}")
async def lock_university(
    university_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find shortlisted university
    shortlisted = db.query(ShortlistedUniversity).filter(
        ShortlistedUniversity.user_id == current_user.id,
        ShortlistedUniversity.university_id == university_id
    ).first()
    
    if not shortlisted:
        raise HTTPException(status_code=404, detail="University not shortlisted")
    
    # Get university and profile
    university = db.query(University).filter(University.id == university_id).first()
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    # Lock university
    shortlisted.is_locked = True
    shortlisted.locked_at = datetime.utcnow()
    
    # Update user stage
    if profile.current_stage != UserStage.PREPARING_APPLICATIONS:
        profile.current_stage = UserStage.PREPARING_APPLICATIONS
    
    # Generate application-specific tasks
    generate_application_tasks(db, current_user.id, university, profile)
    
    # Initialize required documents
    initialize_required_documents(db, current_user.id, shortlisted.id)
    
    db.commit()
    
    return {
        "message": f"University locked successfully! {7} application tasks have been added to your to-do list.",
        "university_id": university_id,
        "tasks_generated": 7
    }

@router.post("/unlock/{university_id}")
async def unlock_university(
    university_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find shortlisted university
    shortlisted = db.query(ShortlistedUniversity).filter(
        ShortlistedUniversity.user_id == current_user.id,
        ShortlistedUniversity.university_id == university_id
    ).first()
    
    if not shortlisted:
        raise HTTPException(status_code=404, detail="University not shortlisted")
    
    # Unlock university
    shortlisted.is_locked = False
    shortlisted.locked_at = None
    
    # Check if there are any other locked universities
    other_locked = db.query(ShortlistedUniversity).filter(
        ShortlistedUniversity.user_id == current_user.id,
        ShortlistedUniversity.is_locked == True
    ).first()
    
    # Update user stage: if no other locked universities, revert to FINALIZING
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile and not other_locked:
        profile.current_stage = UserStage.FINALIZING
    
    db.commit()
    
    return {"message": "University unlocked successfully", "university_id": university_id}

@router.delete("/shortlist/{university_id}")
async def remove_shortlist(
    university_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shortlisted = db.query(ShortlistedUniversity).filter(
        ShortlistedUniversity.user_id == current_user.id,
        ShortlistedUniversity.university_id == university_id
    ).first()
    
    if not shortlisted:
        raise HTTPException(status_code=404, detail="University not shortlisted")
    
    # Delete associated tasks for this university
    university = db.query(University).filter(University.id == university_id).first()
    if university:
        db.query(TodoItem).filter(
            TodoItem.user_id == current_user.id,
            TodoItem.title.like(f'%{university.name}%')
        ).delete()

    # Delete associated documents for this shortlist
    db.query(UniversityDocument).filter(
        UniversityDocument.user_id == current_user.id,
        UniversityDocument.shortlisted_university_id == shortlisted.id
    ).delete()
    
    # Delete the shortlist entry
    db.delete(shortlisted)
    db.commit()
    
    return {"message": "University removed from shortlist"}
