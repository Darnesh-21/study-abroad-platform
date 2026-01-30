from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, UserProfile, ChatMessage, ShortlistedUniversity, University
from app.schemas import ChatMessageCreate, ChatMessageResponse
from app.auth_utils import get_current_user
import logging
# Set up logging
logger = logging.getLogger(__name__)
router = APIRouter()
# Predefined questions for AI Counselor focused on university selection and visa
PREDEFINED_QUESTIONS = {
    "university_selection": {
        "title": " How do I choose the right university?",
        "description": "Get AI guidance on selecting universities based on your profile, goals, and preferences"
    },
    "university_comparison": {
        "title": " How do I compare different universities?",
        "description": "Learn how to evaluate and compare universities across rankings, costs, and specializations"
    },
    "visa_requirements": {
        "title": "️ What are the visa requirements?",
        "description": "Understand visa processes and documentation needed for your desired destination"
    },
    "visa_timeline": {
        "title": " How long does visa processing take?",
        "description": "Learn about visa processing timelines and when to apply"
    },
    "application_strategy": {
        "title": " What's my application strategy?",
        "description": "Get a personalized application plan based on your profile and target universities"
    },
    "top_universities_suggested": {
        "title": "⭐ Top Universities suggested for me",
        "description": "See the top 5 universities recommended based on your profile and preferences"
    }
}
def remove_divider_lines(text: str) -> str:
    """Remove decorative horizontal lines from responses"""
    lines = text.split('\n')
    filtered_lines = []
    for line in lines:
        trimmed = line.strip()
        # Skip lines that are only decorative characters (no actual content)
        is_divider = trimmed and all(c in '━─═─_=*~┃│║╋┣┫┳┻' for c in trimmed)
        if not is_divider:
            filtered_lines.append(line)
    return '\n'.join(filtered_lines)
def generate_personalized_response(user: User, profile: UserProfile, db: Session, question_type: str) -> str:
    """Generate tailored responses based on user's actual profile data"""
    
    if question_type == "university_selection":
        years_until_target = profile.target_intake_year - 2026
        gpa_strength = "Strong" if profile.gpa_percentage and profile.gpa_percentage >= 3.5 else "Good" if profile.gpa_percentage and profile.gpa_percentage >= 3.0 else "Average"
        
        return remove_divider_lines(f""" HOW TO CHOOSE THE RIGHT UNIVERSITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 YOUR PROFILE SNAPSHOT
Current Status:
  • Education: {profile.current_education_level} in {profile.degree_major}
  • Graduating: {profile.graduation_year}
  • GPA: {profile.gpa_percentage}% ({gpa_strength}) 
Target Goals:
  • Degree: {profile.intended_degree} in {profile.field_of_study}
  • Intake Year: {profile.target_intake_year}
  • Preparation Time: {years_until_target} years 
Financial Reality:
  • Annual Budget: ${profile.budget_min:,} - ${profile.budget_max:,}
  • Total Program Cost: ${profile.budget_min * (years_until_target + 2):,} - ${profile.budget_max * (years_until_target + 2):,}
  • Preferred Countries: {profile.preferred_countries or 'Not specified'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PERSONALIZED SELECTION STRATEGY
1️⃣ FILTER BY BUDGET (Most Important for YOU)
   Your budget limits you to specific countries:
   
    Canada: ${20000:,}-${30000:,}/year (Excellent!)
     - Strong programs across fields
     - Good post-grad work visas
     - Reasonable quality of life
   
    Australia: ${25000:,}-${35000:,}/year (Great!)
     - Top universities
     - Good internship opportunities
     - Post-study work visa available
   
    UK: ${20000:,}-${40000:,}/year (Good)
     - 1-year programs save costs
     - Top-ranked universities
     - Great career prospects
   
   ️ USA: ${40000:,}-${60000:,}/year (Stretch)
     - Some public universities fit budget
     - Need scholarships or loans
     - Best long-term ROI
2️⃣ ACADEMIC FIT
   With your {profile.gpa_percentage}% GPA:
   • You're competitive for mid-tier to good universities
   • Focus on programs in {profile.field_of_study}
   • Look for research opportunities that interest you
   • Consider your test score levels (IELTS/TOEFL, GRE/GMAT)
3️⃣ LOCATION SELECTION
   Consider:
   • English-speaking countries (easier transition)
   • Time zone relative to home
   • Cultural environment
   • Cost of living match with budget
4️⃣ UNIVERSITY DIVERSITY STRATEGY
   Apply to a mix:
   
    Dream Universities (3-4):
      - Top-ranked, competitive entry
      - Your {profile.field_of_study} field strength
      - Reach goals
   
   ⭐ Target Universities (5-7):
      - Aligned with your profile
      - Good acceptance probability
      - Strong programs
   
    Safety Universities (3-4):
      - Higher acceptance rates
      - Good quality
      - Reliable backup options
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 YOUR ACTION PLAN (Next 3 Months)
□ Research 15-20 universities in your countries
□ Filter by: budget, rankings, programs in {profile.field_of_study}
□ Shortlist 10-12 universities (dream/target/safe mix)
□ Join university forums and connect with current students
□ Start test prep if not done (IELTS/TOEFL, GRE/GMAT)
□ Prepare Statement of Purpose (SOP)
□ Identify recommender professors
 You have {years_until_target} years - plenty of time to prepare!""")
    elif question_type == "university_comparison":
        shortlisted = db.query(ShortlistedUniversity).filter(
            ShortlistedUniversity.user_id == user.id
        ).all()
        
        uni_count = len(shortlisted)
        
        response = f""" HOW TO COMPARE UNIVERSITIES - YOUR SHORTLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 YOUR SHORTLISTED UNIVERSITIES: {uni_count} total
"""
        if uni_count > 0:
            response += "\n"
            for s in shortlisted[:5]:
                response += f"  • {s.university.name} ({s.university.country}) - {s.category.value}\n"
            if uni_count > 5:
                response += f"\n  ... and {uni_count - 5} more universities\n"
        else:
            response += "\n  (No universities shortlisted yet)\n"
        
        response += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 KEY COMPARISON FACTORS
1️⃣ ACADEMIC QUALITY
   • Program ranking in {profile.field_of_study}
   • Faculty expertise in your field
   • Curriculum and specializations available
   • Industry partnerships and internships
2️⃣ COST ANALYSIS (YOUR BUDGET: ${profile.budget_min:,}-${profile.budget_max:,}/year)
   • Tuition fees
   • Living expenses in that city
   • Available scholarships
   • Cost of living index
   • Return on Investment (ROI)
3️⃣ LOCATION & LIFESTYLE
   • Climate and culture
   • Student community
   • Safety and healthcare
   • Quality of life
   • Distance from {profile.preferred_countries or 'home'}
4️⃣ CAREER & WORK VISA
   • Work visa availability after graduation
   • Employer recognition in target countries
   • Alumni network strength
   • Graduate employment rates
   • Salary outcomes in your field
5️⃣ YOUR TIMELINE
   • Intake year: {profile.target_intake_year}
   • Application deadline
   • Program duration
   • Time to prepare and save funds
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 COMPARISON SCORECARD METHOD:
1. Create a spreadsheet with universities as columns
2. List 5 factors above as rows
3. Score each 1-5 (5 = best)
4. Weight by importance (multiply by importance %)
5. Calculate total for each university
6. Choose your top 3-4
EXAMPLE WEIGHTING (Adjust to YOUR priorities):
- Academic Quality: 25%
- Cost: 25%
- Location: 15%
- Career Outcomes: 25%
- Timeline: 10%
Start comparing now to make an informed decision! """)
        
        return response
    elif question_type == "visa_requirements":
        countries = profile.preferred_countries or "your destination countries"
        target_year = profile.target_intake_year
        
        return remove_divider_lines(f"""️ VISA REQUIREMENTS FOR YOUR STUDY ABROAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Your Target: {countries} | Intake Year: {target_year}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 UNIVERSAL DOCUMENTS (ALL Countries)
You'll need:
 Valid Passport (6+ months validity beyond {target_year})
 University Acceptance Letter (from admitted university)
 Proof of Funds (bank statements showing ${profile.budget_min:,}+)
 Academic Transcripts (official, translated if needed)
 English Proficiency Score (IELTS/TOEFL results)
 Statement of Purpose (SOP - your motivation letter)
 Recommendation Letters (2-3 from professors)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 USA (F-1 STUDENT VISA)
   Processing Time: 4-6 weeks
   Cost: $160
   Special Document: I-20 form (from university)
   Interview: YES - at US embassy
   Work: Limited to 20 hrs/week on-campus
   Post-Study: 12-36 months OPT work permit 
   Your Budget Fit: Some public universities 
 UK (STUDENT VISA)
   Processing Time: 3 weeks (fast!)
   Cost: £325-719 (~${450:,})
   Special Document: Confirmation of Acceptance (CAS)
   Interview: Usually NO 
   Work: 20 hrs/week during studies
   Post-Study: 2-year Graduate Visa 
   Your Budget Fit: Good match! 
 CANADA (STUDY PERMIT)
   Processing Time: 4-8 weeks
   Cost: CAD $150 (~$110)
   Special Document: Letter of Acceptance
   Interview: Possibly
   Work: 20 hrs/week, full-time during breaks 
   Post-Study: 2-3 years work permit 
   Your Budget Fit: Excellent! 
 AUSTRALIA (STUDENT VISA 500)
   Processing Time: 2-4 weeks (fastest!)
   Cost: AUD $575 (~$390)
   Special Document: Confirmation of Enrollment (CoE)
   Interview: Usually NO 
   Work: 20 hrs/week, full-time during breaks 
   Post-Study: Skilled migration options available 
   Your Budget Fit: Very good! 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ YOUR VISA TIMELINE (For Intake {target_year})
By {target_year - 1}:
  □ Complete admission process
  □ Gather documents (transcripts, test scores)
  
Jan-Feb {target_year}:
  □ Request official admission letter + I-20/CAS/CoE
  □ Arrange proof of funds
  
Feb-Mar {target_year}:
  □ Medical examination (if required)
  □ Police clearance certificate
  □ Submit visa application
  
Mar-Apr {target_year}:
  □ Attend visa interview (if required)
  □ Receive visa approval
  
May-Jun {target_year}:
  □ Book flights
  □ Arrange accommodation
  □ Pre-departure orientation
 Key Tips:
  • Start gathering documents NOW - universities are slow!
  • Don't delay medical exams
  • Apply for visa at least 2 months before intake
  • Have buffer time for unexpected delays""")
    elif question_type == "visa_timeline":
        target_year = profile.target_intake_year
        countries = profile.preferred_countries or "your destination"
        
        return remove_divider_lines(f"""⏱️ YOUR VISA PROCESSING TIMELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Target Intake: {target_year}
 Countries: {countries}
 Budget: ${profile.budget_min:,}-${profile.budget_max:,}/year
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏳ PROCESSING TIMES BY COUNTRY
 USA (F-1): 4-6 weeks
   └─ Peak season: 6-12 weeks
   └─ Interview required ️
 UK: 3 weeks (FAST!)
   └─ Standard service: 3-5 weeks
   └─ No interview usually 
 Canada: 4-8 weeks
   └─ Express: 2-4 weeks (extra fee)
   └─ Interview: Sometimes
 Australia: 2-4 weeks (FASTEST!)
   └─ Usually auto-approved 
   └─ No interview 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 YOUR MONTH-BY-MONTH PLAN
 {target_year - 1} AUGUST-SEPTEMBER (NOW!)
   Status: Decision window
   What to do:
    University offers coming in (hopefully!)
    Accept offer at 1-2 universities
    Contact universities for visa documents
    Start document gathering
   
    Action List:
      □ Email university international office
      □ Request admission letter + I-20/CAS/CoE
      □ Ask what documents they need
      □ Start collecting transcripts
 {target_year - 1} SEPTEMBER-OCTOBER (PREPARE)
   Status: Document gathering phase
   What to do:
    Receive I-20/CAS/CoE from university
    Gather all supporting documents
    Arrange proof of funds (${profile.budget_min:,}+)
    Medical examination (if required)
    Police clearance (if required)
   
    Checklist:
      □ Academic transcripts (official)
      □ Test scores (TOEFL/IELTS/GMAT/GRE)
      □ Bank statements (3 months recent)
      □ Sponsor's income proof (if applicable)
      □ Medical exam results
      □ Medical insurance quote
      □ Passport photocopy
      □ Birth certificate (some countries)
 {target_year - 1} OCTOBER-NOVEMBER (APPLY)
   Status: Visa application submission window
   What to do:
    Compile complete application packet
    SUBMIT VISA APPLICATION
    Pay application fee
    Book biometric/visa interview appointment
   
    Expected Processing:
      └─ UK: Decision by mid-December
      └─ Australia: Decision by mid-December
      └─ Canada: Decision by late December
      └─ USA: Decision by January-February
 {target_year - 1} NOVEMBER-DECEMBER (INTERVIEW)
   Status: Interview & approval window
   What to do:
    Attend visa interview (if required)
    Monitor application status
    Prepare to celebrate approval! 
   
    If Approved:
      □ Check visa sticker in passport
      □ Screenshot digital approval
      □ Book flights immediately
      □ Secure accommodation
      □ Arrange travel insurance
      □ Open bank account (if needed)
 {target_year - 1} DECEMBER-JANUARY (FINALIZE)
   Status: Final preparations
   What to do:
    Book flights (prices rise - book NOW!)
    Confirm accommodation
    Arrange travel insurance
    Exchange currency
    Notify bank of travel dates
   
    Pre-Departure:
      □ Check visa expiry date
      □ Download all documents to phone
      □ Join university WhatsApp group
      □ Connect with roommates online
      □ Download offline maps
      □ Arrange airport pickup/taxi
 {target_year} JANUARY-FEBRUARY (TRAVEL)
   Status: Intake period!
   What to do:
    Arrive 1 week before orientation
    Settle into accommodation
    Attend orientation
    Register for classes
    Make friends! 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
️ TIMELINE VARIATIONS
 You Can Go FASTER If:
    Straightforward case (no complications)
    Complete financial proof ready
    No previous visa rejections
   └─ Can apply 1.5 months before intake
 You Need EXTRA TIME If:
    First-time student visa applicant
    Previous visa rejections
    Complex financial situation
    Medical exam required (add 2-3 weeks)
   └─ Apply 3.5-4 months before intake
 URGENT ACTIONS (Do This WEEK):
   1. Contact shortlisted universities
   2. Request admission letter + I-20/CAS/CoE
   3. Gather financial documents
   4. Check passport expiry (must be +6 months)
   5. Download visa requirements for each country
 KEY SUCCESS TIPS:
   • Apply EARLY - don't wait for all documents
   • Incomplete applications often get approved
   • Keep track of each university's deadline
   • Save all confirmation emails & tracking numbers
   • Call/email if application status stagnates
   • Budget extra 2 weeks just in case""")
    elif question_type == "application_strategy":
        shortlisted = db.query(ShortlistedUniversity).filter(
            ShortlistedUniversity.user_id == user.id
        ).all()
        
        dream = len([s for s in shortlisted if s.category.value == "DREAM"])
        target = len([s for s in shortlisted if s.category.value == "TARGET"])
        safe = len([s for s in shortlisted if s.category.value == "SAFE"])
        total = len(shortlisted)
        
        return remove_divider_lines(f""" YOUR PERSONALIZED APPLICATION STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 YOUR PROFILE SUMMARY
 Educational Background:
   Currently: {profile.current_education_level} in {profile.degree_major}
   GPA: {profile.gpa if profile.gpa else 'Not shared'}
   Graduating: {profile.graduation_year}
 Target Program:
   Degree: {profile.intended_degree}
   Major: {profile.field_of_study}
   Intake: {profile.target_intake_year}
 Budget: ${profile.budget_min:,}-${profile.budget_max:,}/year
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 YOUR UNIVERSITY DISTRIBUTION
Total Shortlisted: {total} universities
 DREAM UNIVERSITIES (Reach): {dream}
   └─ Acceptance rate: Usually <15%
   └─ Require: Exceptional profile, strong essays
   └─ Strategy: Apply even if profile seems borderline
   └─ Why: You never know! Some scholarship opportunities!
 TARGET UNIVERSITIES (Match): {target}
   └─ Acceptance rate: 15-40%
   └─ Require: Profile aligned with requirements
   └─ Strategy: Majority of applications here
   └─ Why: Good chance + strong academic fit
 SAFE UNIVERSITIES (Safety): {safe}
   └─ Acceptance rate: Usually >40%
   └─ Require: Meeting minimum requirements
   └─ Strategy: At least 3-4 of these
   └─ Why: Guaranteed admission backup plan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 RECOMMENDED APPLICATION PORTFOLIO
For YOUR profile ({total} universities), we recommend:
Target Distribution:
 Apply to ALL {dream} Dream universities
 Apply to {max(5, target)} Target universities
 Apply to {max(4, safe)} Safe universities
───────────────────────────────
 TOTAL: {dream + max(5, target) + max(4, safe)} applications
This gives you:
• 15-20% acceptance rate from dreams = possible admits 
• 50-70% acceptance rate from targets = likely admits 
• 70%+ acceptance rate from safeties = guaranteed backup 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 YOUR APPLICATION TIMELINE
 PHASE 1: PREPARATION ({profile.target_intake_year - 1} AUGUST-SEPTEMBER)
   Time to start: THIS MONTH!
   
   Week 1-2: Organize
   □ Create spreadsheet for all universities
   □ Note each deadline, requirements, fees
   □ Assign yourself to teams (apps, essays, references)
   
   Week 3-4: Research
   □ Visit each university website
   □ Read recent program reviews on Reddit/YouTube
   □ Note specific interests (professors, clubs, labs, facilities)
   □ Prepare personalized talking points for each
   
    Goal: Be ready to START applications by Sept 1
 PHASE 2: EARLY APPLICATIONS ({profile.target_intake_year - 1} SEPTEMBER-OCTOBER)
   Target: Submit 50% of applications here
   
    Write personalized SOP for first wave (Dream + Target)
    Mention 2-3 specific things per university
    Request recommendation letters from professors
    Gather official transcripts
    Take final English proficiency test
   
   Example SOP personalization:
   "I'm particularly interested in your lab work with [specific
    topic] led by Professor [name], as my research on [X] 
    relates directly. Your program's emphasis on [specific track]
    aligns perfectly with my goal to work on [Y] problems."
   
    Goal: Submit 6-8 applications by end of October
 PHASE 3: REGULAR APPLICATIONS ({profile.target_intake_year - 1} OCTOBER-NOVEMBER)
   Target: Submit remaining applications here
   
    Continue with Target and Safe university applications
    Adjust essays based on university's focus
    Ensure all transcripts requested
    Finalize test scores submission
    Double-check all requirements per university
   
    Goal: All applications submitted by Nov 30
 PHASE 4: DECISIONS ({profile.target_intake_year} JANUARY-APRIL)
   Timeline: Decisions roll in waves
   
    Monitor email closely (check spam folder!)
    Accept admission offers
    Request financial aid information
    Ask waitlisted universities for update (if applicable)
    Compare final offers (tuition, scholarships, location)
   
    Goal: Choose university by April 30
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
️ ESSAY WRITING FORMULA (For Each University)
Do NOT use the same SOP for all universities!
Instead, follow this formula:
1. Paragraph 1: Why YOUR field? (personal motivation)
2. Paragraph 2: Why THIS university? (specific details!)
3. Paragraph 3: What will you contribute? (unique value)
4. Paragraph 4: Post-graduation plans (career aspirations)
Example personalization points:
- Specific professors you want to work with
- Unique programs/tracks the university offers
- Alumni who succeeded in your target field
- Internship opportunities in the city
- Clubs/research centers aligned with your interests
- Scholarship opportunities (if applicable)
 Pro Tip: The more specific you are, the higher your
   chances. Universities want students who CHOSE them, not
   students who applied to everyone.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 RECOMMENDATION LETTERS
Most important component of your application!
Who to ask (in order of preference):
1️⃣ Graduate advisor or thesis supervisor (BEST)
2️⃣ Program coordinator or department head
3️⃣ Professor who taught you in major courses
4️⃣ Internship supervisor (if relevant)
 NOT recommended:
   └─ High school teachers (too old)
   └─ Relatives or friends (not credible)
   └─ Generic templates (obvious to admissions)
How to ask:
 Ask IN PERSON (not email first)
 Provide: Program details, your CV, SOP draft
 Give 2-4 weeks notice minimum
 Send email reminder 1 week before deadline
 Thank them with a card after admission
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 COSTS & BUDGETING
Application fees: ${dream * 150:,}-${dream * 300:,} (Dream unis)
                 ${target * 100:,}-${target * 200:,} (Target unis)
                 ${safe * 50:,}-${safe * 100:,} (Safety unis)
                 ──────────────────────────
Total: Approximately ${total * 150:,}-${total * 250:,}
Budget tip: Some universities offer fee waivers for
international students - ASK!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 FINAL SUCCESS TIPS
 Start early - September applications get 30% better results
 Follow each university's requirements EXACTLY (don't skip steps)
 Write unique essays (not copy-paste between universities)
 Get strong recommendation letters (quality > quantity)
 Meet ALL deadlines (late submissions = automatic rejection)
 Keep backup copies of everything
 Track application status in your spreadsheet
 Don't compare with friends (different profiles, different results)
 Stay positive and patient (decisions take time)
 Prepare for multiple outcomes (dream, target, and safety)
 You've got this! Your profile is solid for your target
   universities. Now make sure your application shows why
   each university should choose YOU! """)
    elif question_type == "top_universities_suggested":
        # Get top 5 recommended universities based on user preferences
        recommended = []
        
        if profile.preferred_countries:
            countries_list = [c.strip() for c in profile.preferred_countries.split(',')]
            recommended = db.query(University).filter(
                University.country.in_(countries_list)
            ).order_by(University.ranking).limit(5).all()
        
        # If no results from preferences, get top 5 globally
        if not recommended:
            recommended = db.query(University).order_by(University.ranking).limit(5).all()
        
        uni_list = "\n".join([f"  {i+1}. {uni.name} - {uni.country} | Ranking: #{uni.ranking}" for i, uni in enumerate(recommended)])
        
        return remove_divider_lines(f"""⭐ TOP UNIVERSITIES SUGGESTED FOR YOU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 YOUR PREFERENCES:
   • Countries: {profile.preferred_countries or 'All countries'}
   • Degree: {profile.intended_degree}
   • Field: {profile.field_of_study}
   • Budget: ${profile.budget_min:,}-${profile.budget_max:,}/year
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 TOP 5 UNIVERSITIES FOR YOU:
{uni_list}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 NEXT STEPS:
   1. Click on each university to explore more details
   2. Compare program offerings and specializations
   3. Check application requirements and deadlines
   4. Review tuition fees and scholarship availability
   5. Add to your shortlist to track progress
 PRO TIP:
   The universities above match your profile and preferences.
   Don't miss out on hidden gems - explore all available options
   in your target countries!""")
    elif question_type == "funding_options":
        years = profile.target_intake_year - 2026 + 2
        total_cost = profile.budget_max * years
        
        return remove_divider_lines(f""" YOUR PERSONALIZED FUNDING STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 YOUR FINANCIAL OVERVIEW
Annual Budget: ${profile.budget_min:,} - ${profile.budget_max:,}
Total Program Cost ({years} years): ${profile.budget_min * years:,} - ${total_cost:,}
Funding Plan: {profile.funding_plan.value.replace('_', ' ').upper() if profile.funding_plan else 'FLEXIBLE'}
Timeline: {profile.target_intake_year - 2026} years to prepare
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 FUNDING OPTIONS RANKED (BEST TO WORST)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 #1: SCHOLARSHIPS & GRANTS ⭐⭐⭐⭐⭐
   (FREE Money - Don't Have to Repay!)
    UNIVERSITY SCHOLARSHIPS
   Offered by: Your admitted universities
   Amount: $5,000-$50,000/year (sometimes full ride!)
   Types:
   ├─ Merit-based: For good grades/test scores
   │  └─ Your GPA: Likely competitive 
   ├─ Need-based: For financial need
   │  └─ Your budget: May qualify 
   ├─ Program-specific: Engineering, business, etc.
   │  └─ Your field: Check university website
   └─ Diversity scholarships: For underrepresented groups
   
   Success Rate: 30-60% of students get SOME scholarship
   Your Chances: HIGH (especially at target universities)
   Timeline: Apply with admission application
   Action: ASK universities for all available scholarships!
    EXTERNAL SCHOLARSHIPS
   Offered by: Governments, NGOs, corporations, foundations
   Amount: $1,000-$30,000
   Popular platforms:
   ├─ MastersPortal.com (huge database!)
   ├─ FindAScholarship.gov (if applying to USA)
   ├─ British Council Scholarships (UK)
   ├─ Chevening (UK government - competitive)
   ├─ Fulbright (USA - very competitive)
   └─ Check YOUR country's education ministry
   
   Success Rate: 10-20% per application
   Your Strategy: Apply to 10-15 scholarships
   Effort: High (essays + applications) but worth it!
   Timeline: Start applications 8-12 months before intake
   Potential: $5,000-$50,000 (life-changing!)
   
   ACTION PLAN:
   □ Search MastersPortal.com for YOUR field
   □ Filter by country/degree type
   □ Apply to ALL you're eligible for
   □ Follow application instructions EXACTLY
   □ Write strong essays (talk about your goals!)
    RESULTS IF YOU WIN:
      └─ Even one external scholarship: $2,000-15,000
      └─ Plus university scholarship: $5,000-25,000
      └─ Total: Often COVERS most costs! 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 #2: ASSISTANTSHIPS (EARN WHILE YOU STUDY)
   (PAY ME to Work + Study!)
   ‍ TEACHING ASSISTANT (TA)
   Role: Help professors with grading, office hours, labs
   Pay: $12,000-$25,000/year
   Includes: Tuition waiver + stipend (HUGE savings!)
   Hours: 15-20 hours/week
   Qualifications:
   ├─ Good English (your test scores help!)
   ├─ Strong in subject matter
   └─ Good communication skills  (likely for you)
   
   Applications: Direct to department head
   Success Rate: 30-50% for competitive students
   Timeline: Apply with admission application
   Your Chances: GOOD (especially for STEM/business)
    RESEARCH ASSISTANT (RA)
   Role: Help professor with research projects
   Pay: $13,000-$30,000/year
   Includes: Often tuition waiver too!
   Hours: 15-20 hours/week
   Benefits:
   ├─ Build research experience
   ├─ Network with professor
   └─ Publication opportunities! 
   
   Best For: Master's programs (less common in MBA)
   Your Profile: Likely eligible 
   Timeline: Post-admission, direct to research advisor
    OTHER WORK OPPORTUNITIES
   On-campus jobs: $12-20/hour (cafeteria, library, admin)
   Hours: 10-20 hours/week (visa limits)
   Earnings: $5,000-12,000/year
   Easy to get: Higher success rate than TA/RA
   Flexibility: Easy to leave job after graduation
    COMBINED BENEFIT:
      TA + Tuition waiver: Covers most of tuition 
      + Part-time job: Covers living expenses 
      + Scholarships: Extra cushion or buffer 
      
      REALISTIC TOTAL: $15,000-40,000/year
      (Often EXCEEDS annual budget!) 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 #3: EDUCATION LOANS (Borrow Money)
   (Cheapest Borrowing Option)
    GOVERNMENT LOANS (BEST RATES)
   Source: Your home country's education ministry
   Interest Rate: 2-5% (very reasonable!)
   Amount: Up to $40,000-100,000
   Repayment: Starts 6-12 months after graduation
   Term: 10-25 years
   
   EXAMPLES:
    India: NEFT/Education Loans from banks
    Pakistan: Government student loan schemes
    Bangladesh: Education loan programs
   [Check YOUR country's education portal]
   
   Advantage: Low interest + government support
   Timeline: Apply 3-4 months before intake
   Your Option: Highly recommended 
    PRIVATE LOANS (Higher Rates)
   Source: International lenders (Prodigy, CommonBond)
   Interest Rate: 5-12% (more expensive)
   Amount: $20,000-$60,000
   Requires: Co-signer usually
   
   When to Use: If government loan insufficient
   Your Option: Backup plan
    LOAN CALCULATOR FOR YOU:
   Annual Cost: ${profile.budget_max:,}
   Program Duration: {years} years
   Total: ${total_cost:,}
   
   If Scholarships Cover 50%: Borrow ${int(total_cost * 0.25):,}
   If TA/RA Covers 30%: Borrow ${int(total_cost * 0.15):,}
   Final Monthly Payment: ~$200-400 after graduation
   
    REALISTIC: Borrow $10,000-20,000
      (Combined with scholarships + work = DOABLE!) 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4️⃣ #4: PERSONAL SAVINGS + FAMILY SUPPORT
   (Safety Net)
    YOUR SAVINGS PLAN
   Current year: {2026}
   Intake year: {profile.target_intake_year}
   Years to save: {profile.target_intake_year - 2026} years
   Annual budget: ${profile.budget_max:,}/year
   
   Total needed: ${total_cost:,}
   Divide by years: ${int(total_cost / max(1, profile.target_intake_year - 2026)):,}/year
   Monthly target: ${int(total_cost / max(1, profile.target_intake_year - 2026) / 12):,}/month
   
    Smart Saving Strategy:
    Open separate bank account for "Study Abroad"
    Automate monthly transfers
    Invest in low-risk savings (FD/bonds)
    Keep emergency fund separate (3 months expenses)
    Track progress on spreadsheet
   ‍‍ FAMILY SUPPORT
   Ask family for: $5,000-15,000/year
   Plan together: Show commitment with YOUR savings
   Present proposal: Show scholarship applications + plan
   Timeline: Discuss NOW (not last minute!)
   
    COMBINED = STRONG FOUNDATION:
      Your savings: $X
      Family support: $Y
      + Scholarships: Often $5-20k
      + TA/RA: $12-15k
      ───────────────────
      Usually covers most costs! 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 YOUR PERSONALIZED FUNDING MIX
Recommended combination FOR YOU:
 STRATEGY:
1. Primary: University Scholarships
   └─ Target: 20-40% of annual cost
   
2. Secondary: TA/RA Assistantship
   └─ Target: 30-50% of annual cost
   
3. Tertiary: Personal savings + family
   └─ Target: 10-30% of annual cost
   
4. If needed: Education loan
   └─ Target: Cover any remaining gap
 FINANCIAL PROJECTION:
   Annual Cost: ${profile.budget_max:,}
   
   Scholarship: ${int(profile.budget_max * 0.3):,} (30%)
   TA/RA: ${int(profile.budget_max * 0.35):,} (35%)
   Savings+Family: ${int(profile.budget_max * 0.25):,} (25%)
   Loan (if needed): ${max(0, int(profile.budget_max * 0.1)):,} (10%)
   ─────────────────────────────────
    FULLY FUNDED! 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 YOUR ACTION PLAN (Start NOW!)
 IMMEDIATELY (This Month):
   □ Calculate exact total cost for YOUR programs
   □ List 10 potential scholarships to apply for
   □ Research government education loans
   □ Open savings account dedicated to study abroad
   □ Tell family about your study abroad goal
 NEXT 3 MONTHS:
   □ Apply to 5-10 external scholarships
   □ Connect with current students (ask about TA/RA)
   □ Meet with university financial aid office
   □ Finalize government loan application
   □ Start systematic savings plan
 6 MONTHS OUT:
   □ Apply with your admission applications
   □ Mention scholarship interests to universities
   □ Express interest in TA/RA roles
   □ Confirm scholarship application status
   □ Adjust plan based on early decisions
 2 MONTHS BEFORE INTAKE:
   □ Confirm all scholarships awarded
   □ Get official TA/RA offer (if eligible)
   □ Finalize all funding sources
   □ Arrange international student loan (if needed)
   □ Plan budget for first semester
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 FINAL SUCCESS TIPS
 DO THIS:
   • Apply for EVERY scholarship you qualify for
   • Get strong recommendation letters for scholarships
   • Write compelling scholarship essays (tell your story!)
   • Ask universities about TA/RA during admission process
   • Start savings NOW (compound interest helps!)
   • Keep excellent grades (scholarships = merit-based)
   • Network with current students for insider tips
   • Consider less expensive countries/universities first
 AVOID:
   • Relying on ONE scholarship source (too risky)
   • Expensive education loans (high interest debt)
   • Borrowing more than necessary
   • Waiting until last minute (fewer options)
   • Ignoring government loan programs (usually cheapest)
   • Overspending once abroad (stick to budget!)
 KEY INSIGHT:
   Most students use COMBINATION of funding:
   Scholarships + Work + Savings + Small loan
   
   RARELY rely on ONE source
   
   Your goal: Mix 3-4 funding sources
   Result: Your dream university WITHIN REACH! 
 YOU CAN AFFORD THIS!
   With planning, savings, and scholarship applications,
   your ${profile.budget_min:,}-${profile.budget_max:,} budget is REALISTIC
   for many great universities worldwide!""")
    else:
        return "I can help with: university selection, visa requirements, application strategy, exam prep, or funding. Which would you like to explore?"
def detect_question_type(message: str) -> str:
    """Detect which type of question the user is asking"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['top university', 'top 5', 'recommended universities', 'suggested universities', 'best universities', 'top universities']):
        return "top_universities_suggested"
    elif any(word in message_lower for word in ['choose', 'select', 'university', 'college', 'which', 'right', 'suitable']):
        return "university_selection"
    elif any(word in message_lower for word in ['compare', 'difference', 'vs', 'versus', 'different']):
        return "university_comparison"
    elif any(word in message_lower for word in ['visa', 'requirement', 'document', 'documentation', 'passport']) and 'timeline' not in message_lower:
        return "visa_requirements"
    elif any(word in message_lower for word in ['visa', 'timeline', 'how long', 'processing', 'when']) and 'requirement' not in message_lower:
        return "visa_timeline"
    elif any(word in message_lower for word in ['application', 'strategy', 'approach', 'plan', 'shortlist']) and 'exam' not in message_lower:
        return "application_strategy"
    
    return None
@router.post("/chat")
async def chat_with_counselor(
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with the AI Counselor - Generates personalized responses from user profile"""
    
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
        return {
            "conversation": [
                {
                    "id": error_msg.id,
                    "role": error_msg.role,
                    "message": error_msg.message,
                    "created_at": error_msg.created_at
                }
            ]
        }
    
    # Save user message
    user_message = ChatMessage(
        user_id=current_user.id,
        role="user",
        message=message_data.message
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    try:
        # Detect question type
        question_type = detect_question_type(message_data.message)
        
        # Generate personalized response based on user profile
        if question_type:
            response_text = generate_personalized_response(current_user, profile, db, question_type)
        else:
            response_text = """I can help with these topics:
 University selection
 University comparison
️ Visa requirements & timelines
 Application strategy
 Exam preparation
 Funding & scholarships
 Career outcomes
Which would you like to explore?"""
        
        # Save AI response
        ai_message = ChatMessage(
            user_id=current_user.id,
            role="assistant",
            message=response_text
        )
        db.add(ai_message)
        db.commit()
        db.refresh(ai_message)
        
        # Return both user and AI messages
        return {
            "conversation": [
                {
                    "id": user_message.id,
                    "role": user_message.role,
                    "message": user_message.message,
                    "created_at": user_message.created_at
                },
                {
                    "id": ai_message.id,
                    "role": ai_message.role,
                    "message": ai_message.message,
                    "created_at": ai_message.created_at
                }
            ]
        }
        
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
        
        return {
            "conversation": [
                {
                    "id": user_message.id,
                    "role": user_message.role,
                    "message": user_message.message,
                    "created_at": user_message.created_at
                },
                {
                    "id": error_message.id,
                    "role": error_message.role,
                    "message": error_message.message,
                    "created_at": error_message.created_at
                }
            ]
        }
@router.get("/questions")
async def get_predefined_questions(
    current_user: User = Depends(get_current_user)
):
    """Get list of predefined questions for the AI Counselor"""
    return {
        "questions": [
            {
                "id": "university_selection",
                "title": PREDEFINED_QUESTIONS["university_selection"]["title"],
                "description": PREDEFINED_QUESTIONS["university_selection"]["description"],
                "suggested_message": "How do I choose the right university for my profile?"
            },
            {
                "id": "university_comparison",
                "title": PREDEFINED_QUESTIONS["university_comparison"]["title"],
                "description": PREDEFINED_QUESTIONS["university_comparison"]["description"],
                "suggested_message": "How do I compare different universities?"
            },
            {
                "id": "visa_requirements",
                "title": PREDEFINED_QUESTIONS["visa_requirements"]["title"],
                "description": PREDEFINED_QUESTIONS["visa_requirements"]["description"],
                "suggested_message": "What are the visa requirements for my destination?"
            },
            {
                "id": "visa_timeline",
                "title": PREDEFINED_QUESTIONS["visa_timeline"]["title"],
                "description": PREDEFINED_QUESTIONS["visa_timeline"]["description"],
                "suggested_message": "How long does visa processing take?"
            },
            {
                "id": "application_strategy",
                "title": PREDEFINED_QUESTIONS["application_strategy"]["title"],
                "description": PREDEFINED_QUESTIONS["application_strategy"]["description"],
                "suggested_message": "What should be my application strategy?"
            },
            {
                "id": "top_universities_suggested",
                "title": PREDEFINED_QUESTIONS["top_universities_suggested"]["title"],
                "description": PREDEFINED_QUESTIONS["top_universities_suggested"]["description"],
                "suggested_message": "What are the top universities suggested for me?"
            }
        ]
    }
@router.get("/history", response_model=List[ChatMessageResponse])
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get chat history for the current user"""
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
    """Clear chat history for the current user"""
    db.query(ChatMessage).filter(ChatMessage.user_id == current_user.id).delete()
    db.commit()
    
    return {"message": "Chat history cleared successfully"}
