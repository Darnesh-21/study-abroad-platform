from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class UserStage(enum.Enum):
    BUILDING_PROFILE = "BUILDING_PROFILE"
    DISCOVERING_UNIVERSITIES = "DISCOVERING_UNIVERSITIES"
    FINALIZING_UNIVERSITIES = "FINALIZING_UNIVERSITIES"
    PREPARING_APPLICATIONS = "PREPARING_APPLICATIONS"

class ProfileStrength(enum.Enum):
    STRONG = "STRONG"
    AVERAGE = "AVERAGE"
    WEAK = "WEAK"

class ExamStatus(enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class FundingType(enum.Enum):
    SELF_FUNDED = "SELF_FUNDED"
    SCHOLARSHIP_DEPENDENT = "SCHOLARSHIP_DEPENDENT"
    LOAN_DEPENDENT = "LOAN_DEPENDENT"

class UniversityCategory(enum.Enum):
    DREAM = "DREAM"
    TARGET = "TARGET"
    SAFE = "SAFE"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    shortlisted_universities = relationship("ShortlistedUniversity", back_populates="user")
    todos = relationship("TodoItem", back_populates="user")
    chat_messages = relationship("ChatMessage", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Onboarding completion
    onboarding_completed = Column(Boolean, default=False)
    current_stage = Column(Enum(UserStage), default=UserStage.BUILDING_PROFILE)
    
    # Academic Background
    current_education_level = Column(String)  # Bachelor's, Master's, etc.
    degree_major = Column(String)
    graduation_year = Column(Integer)
    gpa_percentage = Column(Float, nullable=True)
    
    # Study Goal
    intended_degree = Column(String)  # Bachelor's, Master's, MBA, PhD
    field_of_study = Column(String)
    target_intake_year = Column(Integer)
    preferred_countries = Column(Text)  # JSON array stored as text
    
    # Budget
    budget_min = Column(Float)
    budget_max = Column(Float)
    funding_plan = Column(Enum(FundingType))
    
    # Exams & Readiness
    ielts_toefl_status = Column(Enum(ExamStatus), default=ExamStatus.NOT_STARTED)
    ielts_toefl_score = Column(Float, nullable=True)
    gre_gmat_status = Column(Enum(ExamStatus), default=ExamStatus.NOT_STARTED)
    gre_gmat_score = Column(Float, nullable=True)
    sop_status = Column(Enum(ExamStatus), default=ExamStatus.NOT_STARTED)
    
    # Profile Strength (AI-generated)
    academic_strength = Column(Enum(ProfileStrength), nullable=True)
    exam_strength = Column(Enum(ProfileStrength), nullable=True)
    overall_strength = Column(Enum(ProfileStrength), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="profile")

class University(Base):
    __tablename__ = "universities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String)
    ranking = Column(Integer, nullable=True)
    acceptance_rate = Column(Float, nullable=True)
    tuition_fee_min = Column(Float)
    tuition_fee_max = Column(Float)
    fields_offered = Column(Text)  # JSON array
    programs = Column(Text)  # JSON array of programs
    requirements = Column(Text)  # JSON with IELTS, GRE, GPA requirements
    description = Column(Text)
    website_url = Column(String, nullable=True)
    
    # Relationships
    shortlisted_by = relationship("ShortlistedUniversity", back_populates="university")

class ShortlistedUniversity(Base):
    __tablename__ = "shortlisted_universities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    university_id = Column(Integer, ForeignKey("universities.id"))
    
    category = Column(Enum(UniversityCategory))  # Dream, Target, Safe
    is_locked = Column(Boolean, default=False)
    
    # AI-generated insights
    fit_reason = Column(Text)  # Why this university fits
    risk_factors = Column(Text)  # Potential risks
    acceptance_chance = Column(String)  # Low, Medium, High
    cost_level = Column(String)  # Low, Medium, High
    
    created_at = Column(DateTime, default=datetime.utcnow)
    locked_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="shortlisted_universities")
    university = relationship("University", back_populates="shortlisted_by")

class TodoItem(Base):
    __tablename__ = "todo_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    title = Column(String, nullable=False)
    description = Column(Text)
    priority = Column(String)  # High, Medium, Low
    category = Column(String)  # Exams, Documents, Applications, etc.
    is_completed = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)
    
    # AI-generated flag
    ai_generated = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="todos")

class DocumentStatus(enum.Enum):
    DRAFTING = "DRAFTING"
    PENDING = "PENDING"
    READY = "READY"
    UPLOADED = "UPLOADED"

class DocumentType(enum.Enum):
    SOP = "SOP"
    RECOMMENDATION_LETTER = "RECOMMENDATION_LETTER"
    RESUME = "RESUME"
    TRANSCRIPTS = "TRANSCRIPTS"

class UniversityDocument(Base):
    __tablename__ = "university_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    shortlisted_university_id = Column(Integer, ForeignKey("shortlisted_universities.id"))
    
    document_type = Column(Enum(DocumentType))
    status = Column(Enum(DocumentStatus), default=DocumentStatus.DRAFTING)
    due_date = Column(DateTime, nullable=True)
    file_url = Column(String, nullable=True)  # URL of uploaded file
    
    # Additional fields for recommendation letters
    recipient_name = Column(String, nullable=True)  # For rec letters
    submission_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    shortlisted_university = relationship("ShortlistedUniversity")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    role = Column(String)  # user or assistant
    message = Column(Text, nullable=False)
    
    # Action taken by AI (if any)
    action_type = Column(String, nullable=True)  # shortlist_university, add_task, etc.
    action_metadata = Column(Text, nullable=True)  # JSON with action details
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="chat_messages")
