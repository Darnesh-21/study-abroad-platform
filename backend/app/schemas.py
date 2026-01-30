from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import json

# Enums
class UserStageEnum(str, Enum):
    BUILDING_PROFILE = "BUILDING_PROFILE"
    DISCOVERING_UNIVERSITIES = "DISCOVERING_UNIVERSITIES"
    FINALIZING_UNIVERSITIES = "FINALIZING_UNIVERSITIES"
    PREPARING_APPLICATIONS = "PREPARING_APPLICATIONS"

class ProfileStrengthEnum(str, Enum):
    STRONG = "STRONG"
    AVERAGE = "AVERAGE"
    WEAK = "WEAK"

class ExamStatusEnum(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class FundingTypeEnum(str, Enum):
    SELF_FUNDED = "SELF_FUNDED"
    SCHOLARSHIP_DEPENDENT = "SCHOLARSHIP_DEPENDENT"
    LOAN_DEPENDENT = "LOAN_DEPENDENT"

class UniversityCategoryEnum(str, Enum):
    DREAM = "DREAM"
    TARGET = "TARGET"
    SAFE = "safe"

# User Schemas
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Profile Schemas
class OnboardingData(BaseModel):
    # Academic Background
    current_education_level: str
    degree_major: str
    graduation_year: int
    gpa_percentage: Optional[float] = None
    
    # Study Goal
    intended_degree: str
    field_of_study: str
    target_intake_year: int
    preferred_countries: List[str]
    
    # Budget
    budget_min: float
    budget_max: float
    funding_plan: FundingTypeEnum
    
    # Exams
    ielts_toefl_status: ExamStatusEnum
    ielts_toefl_score: Optional[float] = None
    gre_gmat_status: ExamStatusEnum
    gre_gmat_score: Optional[float] = None
    sop_status: ExamStatusEnum

class ProfileUpdate(BaseModel):
    current_education_level: Optional[str] = None
    degree_major: Optional[str] = None
    graduation_year: Optional[int] = None
    gpa_percentage: Optional[float] = None
    intended_degree: Optional[str] = None
    field_of_study: Optional[str] = None
    target_intake_year: Optional[int] = None
    preferred_countries: Optional[List[str]] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    funding_plan: Optional[FundingTypeEnum] = None
    ielts_toefl_status: Optional[ExamStatusEnum] = None
    ielts_toefl_score: Optional[float] = None
    gre_gmat_status: Optional[ExamStatusEnum] = None
    gre_gmat_score: Optional[float] = None
    sop_status: Optional[ExamStatusEnum] = None

class ProfileResponse(BaseModel):
    id: int
    onboarding_completed: bool
    current_stage: UserStageEnum
    current_education_level: Optional[str]
    degree_major: Optional[str]
    graduation_year: Optional[int]
    gpa_percentage: Optional[float]
    intended_degree: Optional[str]
    field_of_study: Optional[str]
    target_intake_year: Optional[int]
    preferred_countries: Optional[list] = []
    budget_min: Optional[float]
    budget_max: Optional[float]
    funding_plan: Optional[FundingTypeEnum]
    ielts_toefl_status: Optional[ExamStatusEnum]
    ielts_toefl_score: Optional[float]
    gre_gmat_status: Optional[ExamStatusEnum]
    gre_gmat_score: Optional[float]
    sop_status: Optional[ExamStatusEnum]
    academic_strength: Optional[ProfileStrengthEnum]
    exam_strength: Optional[ProfileStrengthEnum]
    overall_strength: Optional[ProfileStrengthEnum]
    
    @field_validator('preferred_countries', mode='before')
    @classmethod
    def parse_countries(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return []
        return v if v else []
    
    class Config:
        from_attributes = True

# University Schemas
class UniversityBase(BaseModel):
    name: str
    country: str
    city: Optional[str]
    ranking: Optional[int]
    acceptance_rate: Optional[float]
    tuition_fee_min: float
    tuition_fee_max: float
    fields_offered: List[str]
    programs: List[str]
    requirements: dict
    description: str
    website_url: Optional[str]

class UniversityResponse(UniversityBase):
    id: int
    
    @field_validator('fields_offered', 'programs', mode='before')
    @classmethod
    def parse_json_list(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
    
    @field_validator('requirements', mode='before')
    @classmethod
    def parse_json_dict(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
    
    class Config:
        from_attributes = True

class ShortlistedUniversityCreate(BaseModel):
    university_id: int
    category: UniversityCategoryEnum

class ShortlistedUniversityResponse(BaseModel):
    id: int
    university_id: int
    category: UniversityCategoryEnum
    is_locked: bool
    fit_reason: Optional[str]
    risk_factors: Optional[str]
    acceptance_chance: Optional[str]
    cost_level: Optional[str]
    created_at: datetime
    locked_at: Optional[datetime]
    university: UniversityResponse
    
    class Config:
        from_attributes = True

# Todo Schemas
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str  # High, Medium, Low
    category: str
    due_date: Optional[datetime] = None

class TodoUpdate(BaseModel):
    is_completed: Optional[bool] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    category: str
    is_completed: bool
    due_date: Optional[datetime]
    ai_generated: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Chat Schemas
class ChatMessageCreate(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    id: int
    role: str
    message: str
    action_type: Optional[str]
    action_metadata: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Document Schemas
class DocumentStatusEnum(str, Enum):
    DRAFTING = "DRAFTING"
    PENDING = "PENDING"
    READY = "READY"
    UPLOADED = "UPLOADED"

class DocumentTypeEnum(str, Enum):
    SOP = "SOP"
    RECOMMENDATION_LETTER = "RECOMMENDATION_LETTER"
    RESUME = "RESUME"
    TRANSCRIPTS = "TRANSCRIPTS"

class UniversityDocumentResponse(BaseModel):
    id: int
    user_id: int
    shortlisted_university_id: int
    document_type: DocumentTypeEnum
    status: DocumentStatusEnum
    due_date: Optional[datetime]
    file_url: Optional[str]
    recipient_name: Optional[str]
    submission_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Dashboard Schemas
class CommittedUniversityData(BaseModel):
    shortlisted_university: ShortlistedUniversityResponse
    tasks: List[TodoResponse]
    documents: List[UniversityDocumentResponse]
    
    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    user: UserResponse
    profile: ProfileResponse
    todos: List[TodoResponse]
    shortlisted_universities: List[ShortlistedUniversityResponse]
    locked_universities_count: int
    committed_universities: List[CommittedUniversityData] = []
