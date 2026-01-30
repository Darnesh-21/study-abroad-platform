from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
import requests
from app.database import get_db
from app.models import User, UserProfile, ChatMessage, TodoItem, ShortlistedUniversity, University
from app.schemas import ChatMessageCreate, ChatMessageResponse
from app.auth_utils import get_current_user
from app.config import get_settings
import logging

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()
settings = get_settings()

# Predefined questions for AI Counselor
PREDEFINED_QUESTIONS = {
    "university_selection": {
        "title": " How do I choose the right university?",
        "description": "Get guidance on selecting universities based on your profile and goals"
    },
    "university_comparison": {
        "title": " How do I compare different universities?",
        "description": "Learn how to evaluate and compare universities for your needs"
    },
    "visa_requirements": {
        "title": "️ What are the visa requirements?",
        "description": "Understand visa processes and documentation needed for your destination"
    },
    "visa_timeline": {
        "title": " How long does visa processing take?",
        "description": "Learn about visa processing timelines and application process"
    },
    "application_process": {
        "title": " What's the application process?",
        "description": "Get step-by-step guidance on the university application process"
    },
    "exam_preparation": {
        "title": " How should I prepare for entrance exams?",
        "description": "Learn effective strategies for preparing for IELTS, TOEFL, GRE, GMAT"
    },
    "funding_options": {
        "title": " What are my funding options?",
        "description": "Explore scholarships, loans, and other funding opportunities"
    },
    "career_path": {
        "title": " How will this course help my career?",
        "description": "Get insights on career outcomes and opportunities after studying abroad"
    }
}

def query_huggingface_api(prompt: str) -> str:
    """Query Hugging Face Mistral API for AI responses"""
    try:
        hf_token = settings.huggingface_token
        if not hf_token:
            logger.error("Hugging Face token not configured")
            return "I'm unable to process your request at the moment. Please try again later."
        
        headers = {"Authorization": f"Bearer {hf_token}"}
        api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "top_p": 0.9,
            }
        }
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            generated_text = result[0].get("generated_text", "")
            # Remove the prompt from the generated text
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            return generated_text if generated_text else "I couldn't generate a response. Please try again."
        
        return "I couldn't generate a response. Please try again."
    
    except requests.exceptions.Timeout:
        logger.error("Hugging Face API timeout")
        return "The request took too long. Please try again."
    except requests.exceptions.RequestException as e:
        logger.error(f"Hugging Face API error: {str(e)}")
        return "I'm having trouble processing your request. Please try again."
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "An unexpected error occurred. Please try again."

def generate_profile_response(user: User, profile: UserProfile, db: Session, question_type: str) -> str:
    """Generate personalized response based on user's profile and question type"""
    
    if question_type == "profile":
        strength = profile.academic_strength.value if profile.academic_strength else "Not assessed"
        exam_strength = profile.exam_strength.value if profile.exam_strength else "Not assessed"
        overall = profile.overall_strength.value if profile.overall_strength else "Not assessed"
        
        response = f"""## Your Profile Assessment

**Academic Foundation:**
- Current Education: {profile.current_education_level} in {profile.degree_major}
- Graduation Year: {profile.graduation_year}
- GPA: {profile.gpa_percentage}%
- Academic Strength: {strength}

**Study Goals:**
- Target Degree: {profile.intended_degree} in {profile.field_of_study}
- Target Intake: {profile.target_intake_year}
- Preferred Countries: {profile.preferred_countries}

**Financial Profile:**
- Budget Range: ${profile.budget_min} - ${profile.budget_max} per year
- Funding Plan: {profile.funding_plan.value if profile.funding_plan else "Not specified"}

**Exam Status:**
- English Proficiency: {profile.ielts_toefl_status.value} (Score: {profile.ielts_toefl_score if profile.ielts_toefl_score else 'Pending'})
- Graduate Exam: {profile.gre_gmat_status.value} (Score: {profile.gre_gmat_score if profile.gre_gmat_score else 'Pending'})
- SOP Status: {profile.sop_status.value}
- Exam Strength: {exam_strength}

**Profile Summary:**
Overall Profile Strength: **{overall}**

**Key Recommendations:**
"""
        if profile.ielts_toefl_status.value == "NOT_STARTED":
            response += "\n Prioritize English proficiency test preparation (IELTS/TOEFL) - this is critical for admission"
        
        if profile.gre_gmat_status.value == "NOT_STARTED":
            response += "\n Schedule GRE/GMAT exam - most programs require this"
        
        if profile.sop_status.value == "NOT_STARTED":
            response += "\n Begin drafting your Statement of Purpose - this is your key differentiator"
        
        response += "\n\nYour profile shows promise! Focus on completing your test scores and SOP to strengthen your applications."
        return response
    
    elif question_type == "universities":
        shortlisted = db.query(ShortlistedUniversity).filter(
            ShortlistedUniversity.user_id == user.id
        ).all()
        
        dream = [s for s in shortlisted if s.category.value == "DREAM"]
        target = [s for s in shortlisted if s.category.value == "TARGET"]
        safe = [s for s in shortlisted if s.category.value == "SAFE"]
        
        response = f"""## University Recommendations for Your Profile

**Your Profile Match:**
- Budget Range: ${profile.budget_min} - ${profile.budget_max}/year
- Target Degree: {profile.intended_degree} in {profile.field_of_study}
- Preferred Countries: {profile.preferred_countries}

**Recommended University Strategy:**

**Dream Universities ({len(dream)} shortlisted) - Apply to 3-4**
- Top tier institutions
- Acceptance Rate: 5-15%
- Requirements: Competitive GPA (3.5+), Test scores (IELTS 7.5+/TOEFL 100+)
"""
        for uni in dream[:3]:
            response += f"\n  • {uni.university.name} ({uni.university.country})"
        
        response += f"""

**Target Universities ({len(target)} shortlisted) - Apply to 6-8**
- Mid to upper tier
- Acceptance Rate: 25-40%
- Your best bet for strong admission chances
"""
        for uni in target[:3]:
            response += f"\n  • {uni.university.name} ({uni.university.country})"
        
        response += f"""

**Safety Universities ({len(safe)} shortlisted) - Apply to 3-4**
- Good backup options
- Acceptance Rate: 50%+
- Easier admission with solid programs
"""
        for uni in safe[:2]:
            response += f"\n  • {uni.university.name} ({uni.university.country})"
        
        response += f"""

**Application Strategy:**
 Total Applications: {len(dream)} Dream + {len(target)} Target + {len(safe)} Safe = {len(dream) + len(target) + len(safe)} universities
 Timeline: Apply September-December for Fall intake
 Customize each application to the specific university
 Highlight how your profile fits each institution's strengths

**Next Steps:**
1. Complete all standardized tests
2. Write tailored SOPs for each university
3. Gather 2-3 strong recommendation letters
4. Submit applications early for best consideration
"""
        return response
    
    elif question_type == "timeline":
        response = f"""## Your Application Timeline & Action Plan

**Current Profile Status:**
- Education: {profile.current_education_level} (Graduating: {profile.graduation_year})
- Test Status: {profile.ielts_toefl_status.value} English, {profile.gre_gmat_status.value} Graduate Exam
- SOP Status: {profile.sop_status.value}

**PHASE 1: Preparation (NOW - 2 months)**

*Immediate Tasks (Next 2 weeks):*
 Register for IELTS/TOEFL exam (book for {6 if profile.ielts_toefl_status.value == 'NOT_STARTED' else 2} weeks out)
 Register for GRE/GMAT if needed (book for {8 if profile.gre_gmat_status.value == 'NOT_STARTED' else 2} weeks out)
 Create application tracking spreadsheet
 Finalize university shortlist (you have {len(db.query(ShortlistedUniversity).filter(ShortlistedUniversity.user_id == user.id).all())} universities)

*Weeks 3-8:*
 Begin/complete test preparation
 Start drafting Statement of Purpose
 Identify 3-4 professors for recommendation letters
 Gather academic transcripts and certificates

**PHASE 2: Testing ({2 if profile.ielts_toefl_status.value == 'NOT_STARTED' else 1}-3 months)**

*Exam Preparation:*
 Weekly practice tests
 Target IELTS: 7.0-7.5 | TOEFL: 95-105 | GRE: 310+ | GMAT: 700+
 Schedule official exams

**PHASE 3: Application Submission (3-4 months)**

*By September:*
 Get official test score reports to universities
 Request recommendation letters
 Finalize and proofread SOPs
 Prepare application fee payments

*Submission:*
 Submit to all {len(db.query(ShortlistedUniversity).filter(ShortlistedUniversity.user_id == user.id).all())} universities
 Keep detailed records
 Track submission confirmations

**PHASE 4: Decisions & Enrollment (4-6 months)**

*Awaiting Results:*
 Monitor email for decisions
 Compare financial aid packages
 Confirm enrollment deposit

*Before Travel:*
 Apply for visa (8-12 weeks before departure)
 Book accommodation
 Purchase travel insurance
 Arrange pre-arrival orientation

Your target intake year is {profile.target_intake_year}. Plan accordingly!
"""
        return response
    
    elif question_type == "budget":
        response = f"""## Budget & Funding Plan for You

**Your Budget Range:** ${profile.budget_min} - ${profile.budget_max} per year
**Funding Plan:** {profile.funding_plan.value if profile.funding_plan else "To be determined"}

**Average Annual Costs by Destination:**
"""
        preferred_countries = profile.preferred_countries.split(",") if profile.preferred_countries else []
        
        costs = {
            "USA": {"tuition": "20,000-50,000", "living": "12,000-25,000", "total": "32,000-75,000"},
            "UK": {"tuition": "15,000-35,000", "living": "12,000-20,000", "total": "27,000-55,000"},
            "Canada": {"tuition": "15,000-30,000", "living": "10,000-18,000", "total": "25,000-48,000"},
            "Australia": {"tuition": "20,000-45,000", "living": "15,000-22,000", "total": "35,000-67,000"},
        }
        
        for country, costs_data in costs.items():
            if any(pref.lower() in country.lower() or country.lower() in pref.lower() for pref in preferred_countries):
                response += f"\n**{country}:** ${costs_data['total']}/year (Tuition: ${costs_data['tuition']}, Living: ${costs_data['living']})"
        
        response += f"""

**Funding Strategy for Your Profile:**

**Option 1: Scholarships (Your Best Bet)**
- Apply to 3-4 universities offering full scholarships
- Apply to 5-6 with partial scholarships
- Search: MastersPortal.com, ScholarshipDB.com
- Your budget suggests seeking {profile.funding_plan.value.lower().replace('_', ' ')} options

**Option 2: Assistantships (TA/RA)**
- Teaching Assistant: $12,000-18,000/year
- Research Assistant: $12,000-20,000/year
- Often covers tuition + living expenses
- Negotiate during admission

**Option 3: Education Loans**
- Home country education loans (low interest)
- Compare: Interest rates, repayment terms
- Typical amount: $10,000-30,000

**Option 4: Personal Savings & Family**
- Most realistic for self-funded students
- Plan 1-2 years in advance
- Calculate: Total Cost × Number of Years

**Your Estimated Total Program Cost:**
"""
        intake_year = profile.target_intake_year
        current_year = 2026
        years = intake_year - current_year + 2
        min_cost = profile.budget_min * years
        max_cost = profile.budget_max * years
        response += f"- Minimum: ${min_cost:,.0f} ({years} years × ${profile.budget_min:,.0f}/year)"
        response += f"\n- Maximum: ${max_cost:,.0f} ({years} years × ${profile.budget_max:,.0f}/year)"
        response += f"""

**Recommendations:**
 Apply to multiple universities with varying aid packages
 Prioritize universities offering scholarships matching your budget
 Plan for 20-30% cost increase due to inflation/currency
 Look for co-op programs to earn while studying
 Consider countries with lower living costs

Your {profile.funding_plan.value.lower().replace('_', ' ')} approach requires strategic university selection and early application!
"""
        return response
    
    elif question_type == "tests":
        response = f"""## Test Preparation Strategy for Your Profile

**Your Current Test Status:**
- English (IELTS/TOEFL): {profile.ielts_toefl_status.value} {f'(Score: {profile.ielts_toefl_score})' if profile.ielts_toefl_score else ''}
- Graduate Exam (GRE/GMAT): {profile.gre_gmat_status.value} {f'(Score: {profile.gre_gmat_score})' if profile.gre_gmat_score else ''}

**Degree Type: {profile.intended_degree} in {profile.field_of_study}**

**English Proficiency Test Required:**

**IELTS vs TOEFL:**
- Cost: $250-300 each
- Processing: 5-7 days
- Target Score: 7.0-7.5 (IELTS) or 95-110 (TOEFL)
- Validity: 2 years

**Graduate Entrance Exam:**
"""
        if "MBA" in profile.intended_degree or "Management" in profile.field_of_study:
            response += """
**GMAT (for MBA programs):**
- Format: 4 sections (3h 7min total)
- Scoring: 200-800
- Cost: $250-275
- Target Score: 700-750 (competitive programs)
- Valid: 5 years
"""
        else:
            response += """
**GRE (for most Master's programs):**
- Format: 3 sections (3h 45min total)
- Scoring: 260-340 (Verbal + Quantitative)
- Cost: $205-220
- Target Score: 310-320 (competitive programs)
- Valid: 5 years
"""
        
        response += f"""

**Personalized Test Prep Timeline for Your Profile:**

*Month 1-2 (Diagnostic Phase):*
 Take diagnostic tests to identify weak areas
 Enroll in prep course if needed (Kaplan, Manhattan Prep, etc.)
 Set target scores: IELTS 7.0+ or TOEFL 100+

*Month 3-4 (Active Preparation):*
 Study 15-20 hours/week
 Weekly practice tests
 Focus on weak sections
 Join study groups

*Month 5 (Full Practice):*
 Full-length practice tests weekly
 Timed conditions
 Analyze mistakes
 Fine-tune test-taking strategy

*Month 6:*
 Take official exam(s)
 Request score reports sent to universities

**Recommended Resources:**
- IELTS: Official IELTS practice books, IDP website
- TOEFL: ETS official materials, Khan Academy partnership
- GRE: ETS Official Guide, Magoosh, Manhattan Prep
- GMAT: Official GMAT Prep Software, Manhattan Prep

**Test Cost Breakdown:**
- English Test: $250-300
- Graduate Exam: $200-250
- Prep Course (optional): $500-2,000
- Total Estimated: $950-2,550

**Timeline to Your Target Year ({profile.target_intake_year}):**
 Complete tests by {profile.target_intake_year - 1} (at least 3-4 months before applications)
 Apply with scores August-December
 Get admission decisions by March-April
 Begin studies in {profile.target_intake_year}

**Next Steps:**
1. Register for IELTS/TOEFL within 2 weeks
2. Register for GRE/GMAT within 4 weeks
3. Start prep course immediately
4. Target completion by {profile.target_intake_year - 1} December
"""
        return response
    
    elif question_type == "visa":
        countries = profile.preferred_countries.split(",") if profile.preferred_countries else ["General"]
        response = f"""## Visa & Documentation Guide for Your Journey

**Your Target Countries:** {profile.preferred_countries if profile.preferred_countries else "To be determined"}
**Target Year:** {profile.target_intake_year}
**Degree:** {profile.intended_degree} in {profile.field_of_study}

**Required Documents (Universal):**

**Academic Documents:**
 Bachelor's degree certificate
 Official transcripts (sealed)
 Degree evaluation (if required)
 Statement of Purpose (500-750 words)
 Academic references (2-3 letters)

**Admission Documents:**
 University acceptance letter
 Proof of financial support
 Program syllabus/details

**Financial Documents:**
 Bank statements (last 3-6 months)
 Evidence of funds: ${profile.budget_min} - ${profile.budget_max} per year for {profile.target_intake_year - 2026 + 2} years
 Scholarship letters (if applicable)
 Proof of sponsorship (if applicable)

**Personal Documents:**
 Valid passport (6+ months validity)
 Birth certificate
 National ID copies
 Medical examination (if required)
 Police clearance certificate

**Country-Specific Guidance:**

**USA (F-1 Visa):**
- Processing Time: 4-6 weeks after I-20
- Cost: $160 visa fee
- Work: 20 hrs/week on campus
- Post-Study: OPT up to 3 years
- Interview: Required at US embassy

**UK (Student Visa):**
- Processing Time: 3 weeks standard
- Cost: £325-719
- Work: 20 hrs/week during studies
- Post-Study: Graduate visa (2-3 years)
- Interview: Not required typically

**Canada (Study Permit):**
- Processing Time: 4-8 weeks
- Cost: CAD $150
- Work: 20 hrs/week on campus, full-time during breaks
- Post-Study: PGWP up to 3 years
- Interview: Not required

**Australia (Student Visa 500):**
- Processing Time: 2-4 weeks
- Cost: AUD $575
- Work: 20 hrs/week during studies, unlimited breaks
- Post-Study: PSW 2-5 years
- Interview: Not required typically

**Your Application & Visa Timeline:**

**By December {profile.target_intake_year - 1}:**
 Submit all applications to universities
 Compile visa-required documents
 Get police clearance

**By February {profile.target_intake_year}:**
 Receive university acceptance
 Request official transcripts & documents
 Book medical examination

**By March-April {profile.target_intake_year}:**
 Collect admission letter
 Compile financial documents
 Submit visa application

**By May-June {profile.target_intake_year}:**
 Attend visa interview (if required)
 Receive visa approval
 Book flights

**By July-August {profile.target_intake_year}:**
 Purchase travel insurance
 Arrange accommodation
 Finalize pre-arrival requirements
 Depart for studies!

**Document Cost Estimate:**
- Passport: $50-100
- Translations & Notarization: $200-400
- Medical Exam: $50-150
- Police Clearance: $30-100
- Visa Fee: $160-720
- Travel Insurance: $200-500
- **Total: $690-1,870**

**Pro Tips for Success:**
 Start gathering documents 3 months before visa application
 Keep both digital and physical copies
 Use certified courier for originals
 Apply for visa as soon as you have admission letter
 Join university international student groups early

Your {profile.intended_degree} program in {profile.field_of_study} intake year {profile.target_intake_year} requires timely visa application. Start preparing now!
"""
        return response
    
    return "Question type not found. Please select from available options."

def get_user_context(user: User, db: Session) -> str:
    """Build context about the user for the AI counselor"""
    
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    
    if not profile or not profile.onboarding_completed:
        return "User has not completed onboarding yet."
    
    context = f"""
User Profile:
- Name: {user.full_name}
- Current Education: {profile.current_education_level} in {profile.degree_major}
- Graduation Year: {profile.graduation_year}
- GPA: {profile.gpa_percentage if profile.gpa_percentage else 'Not provided'}
- Intended Degree: {profile.intended_degree} in {profile.field_of_study}
- Target Intake: {profile.target_intake_year}
- Preferred Countries: {profile.preferred_countries}
- Budget: ${profile.budget_min} - ${profile.budget_max} per year
- Funding Plan: {profile.funding_plan.value if profile.funding_plan else 'Not specified'}

Exam Status:
- IELTS/TOEFL: {profile.ielts_toefl_status.value} (Score: {profile.ielts_toefl_score if profile.ielts_toefl_score else 'N/A'})
- GRE/GMAT: {profile.gre_gmat_status.value} (Score: {profile.gre_gmat_score if profile.gre_gmat_score else 'N/A'})
- SOP: {profile.sop_status.value}

Profile Strength:
- Academic: {profile.academic_strength.value if profile.academic_strength else 'N/A'}
- Exams: {profile.exam_strength.value if profile.exam_strength else 'N/A'}
- Overall: {profile.overall_strength.value if profile.overall_strength else 'N/A'}

Current Stage: {profile.current_stage.value}
"""
    
    # Add shortlisted universities
    shortlisted = db.query(ShortlistedUniversity).filter(
        ShortlistedUniversity.user_id == user.id
    ).all()
    
    if shortlisted:
        context += "\n\nShortlisted Universities:\n"
        for s in shortlisted:
            locked = " (LOCKED)" if s.is_locked else ""
            context += f"- {s.university.name} ({s.category.value}){locked}\n"
    
    # Add pending todos
    todos = db.query(TodoItem).filter(
        TodoItem.user_id == user.id,
        TodoItem.is_completed == False
    ).limit(5).all()
    
    if todos:
        context += "\n\nPending Tasks:\n"
        for todo in todos:
            context += f"- {todo.title} ({todo.priority} priority)\n"
    
    return context

def get_system_prompt() -> str:
    """System prompt for the AI counselor"""
    return """You are an expert study abroad counselor AI assistant. Your role is to:

1. Guide students through their study abroad journey
2. Provide personalized university recommendations based on their profile
3. Explain why specific universities fit their profile
4. Identify risks and opportunities
5. Create actionable tasks and to-do items
6. Answer questions about the application process
7. Help students understand their profile strengths and weaknesses

When recommending universities:
- Categorize them as Dream (reach), Target (match), or Safe (safety)
- Explain WHY each university fits their profile
- Highlight specific risks (cost, competition, requirements)
- Be honest about acceptance chances

When suggesting action items:
- Be specific and actionable
- Set realistic priorities
- Consider the student's current stage

Always be:
- Encouraging but realistic
- Data-driven in your recommendations
- Clear about risks and trade-offs
- Supportive of the student's goals

If asked to shortlist a university or add a task, respond with a structured JSON action in your response.
"""

@router.post("/chat", response_model=ChatMessageResponse)
async def chat_with_counselor(
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if onboarding is completed
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile or not profile.onboarding_completed:
        error_msg = ChatMessage(
            user_id=current_user.id,
            role="assistant",
            message="Please complete your onboarding first to unlock the AI Counselor. I need to understand your background and goals to provide personalized guidance."
        )
        db.add(error_msg)
        db.commit()
        db.refresh(error_msg)
        return error_msg
    
    # Save user message
    user_message = ChatMessage(
        user_id=current_user.id,
        role="user",
        message=message_data.message
    )
    db.add(user_message)
    db.commit()
    
    try:
        # Match user input to predefined questions
        user_input = message_data.message.lower()
        question_type = None
        
        # Map user input to question types
        if any(word in user_input for word in ['profile', 'strength', 'assessment', 'weakness']):
            question_type = "profile"
        elif any(word in user_input for word in ['university', 'recommend', 'which', 'suitable']):
            question_type = "universities"
        elif any(word in user_input for word in ['timeline', 'schedule', 'when', 'deadline', 'application']):
            question_type = "timeline"
        elif any(word in user_input for word in ['budget', 'cost', 'funding', 'money', 'expensive']):
            question_type = "budget"
        elif any(word in user_input for word in ['test', 'exam', 'ielts', 'toefl', 'gre', 'gmat', 'preparation']):
            question_type = "tests"
        elif any(word in user_input for word in ['visa', 'document', 'documentation', 'passport']):
            question_type = "visa"
        
        # If no question type matched, show available options
        if not question_type:
            response_text = """Hello! I'm your AI Counselor. I can help you with these topics:

 **Profile Assessment** - Analyze your strengths and weaknesses
 **University Recommendations** - Get personalized university suggestions  
 **Application Timeline** - See your action plan and deadlines
 **Budget & Funding** - Understand costs and funding options
 **Test Preparation** - Get guidance on IELTS, TOEFL, GRE, GMAT
️ **Visa & Documentation** - Learn about visa requirements

Which topic would you like to explore?"""
        else:
            # Generate personalized response based on user's profile
            response_text = generate_profile_response(current_user, profile, db, question_type)
        
        # Save AI response
        ai_message = ChatMessage(
            user_id=current_user.id,
            role="assistant",
            message=response_text,
            action_type=None,
            action_metadata=None
        )
        db.add(ai_message)
        db.commit()
        db.refresh(ai_message)
        
        return ai_message
        
    except Exception as e:
        logger.error(f"Counselor chat error: {str(e)}", exc_info=True)
        
        error_message = ChatMessage(
            user_id=current_user.id,
            role="assistant",
            message="I apologize, but I encountered an error processing your request. Please try again."
        )
        db.add(error_message)
        db.commit()
        db.refresh(error_message)
        
        return error_message

@router.get("/questions")
async def get_predefined_questions(
    current_user: User = Depends(get_current_user)
):
    """Get list of predefined questions for the AI Counselor"""
    return {
        "questions": [
            {
                "id": "profile",
                "title": PREDEFINED_QUESTIONS["profile"]["title"],
                "description": PREDEFINED_QUESTIONS["profile"]["description"],
                "suggested_message": "Analyze my profile"
            },
            {
                "id": "universities",
                "title": PREDEFINED_QUESTIONS["universities"]["title"],
                "description": PREDEFINED_QUESTIONS["universities"]["description"],
                "suggested_message": "Recommend universities for me"
            },
            {
                "id": "timeline",
                "title": PREDEFINED_QUESTIONS["timeline"]["title"],
                "description": PREDEFINED_QUESTIONS["timeline"]["description"],
                "suggested_message": "Create an application timeline"
            },
            {
                "id": "budget",
                "title": PREDEFINED_QUESTIONS["budget"]["title"],
                "description": PREDEFINED_QUESTIONS["budget"]["description"],
                "suggested_message": "Help me with budget planning"
            },
            {
                "id": "tests",
                "title": PREDEFINED_QUESTIONS["tests"]["title"],
                "description": PREDEFINED_QUESTIONS["tests"]["description"],
                "suggested_message": "Guide me on test preparation"
            },
            {
                "id": "visa",
                "title": PREDEFINED_QUESTIONS["visa"]["title"],
                "description": PREDEFINED_QUESTIONS["visa"]["description"],
                "suggested_message": "Tell me about visa requirements"
            }
        ]
    }

@router.get("/history", response_model=List[ChatMessageResponse])
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).order_by(ChatMessage.created_at.desc()).limit(limit).all()
    
    messages.reverse()
    return messages

@router.delete("/history")
async def clear_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(ChatMessage).filter(ChatMessage.user_id == current_user.id).delete()
    db.commit()
    
    return {"message": "Chat history cleared successfully"}
