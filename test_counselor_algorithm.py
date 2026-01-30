#!/usr/bin/env python3
"""
Quick test script to verify the counselor algorithm works correctly.
This tests the response generation logic without needing to run the full API.
"""

# Mock classes to test the algorithm
class MockUser:
    def __init__(self):
        self.id = 1
        self.full_name = "John Doe"

class MockProfile:
    def __init__(self):
        self.current_education_level = "Bachelor's"
        self.degree_major = "Computer Science"
        self.graduation_year = 2024
        self.intended_degree = "Master's"
        self.field_of_study = "Data Science"
        self.target_intake_year = 2026
        self.preferred_countries = "USA, Canada, UK"
        self.budget_min = 30000
        self.budget_max = 50000
        self.gpa_percentage = 3.6
        self.ielts_toefl_status = type('obj', (object,), {'value': 'Not Taken'})()
        self.ielts_toefl_score = None
        self.gre_gmat_status = type('obj', (object,), {'value': 'Not Taken'})()
        self.gre_gmat_score = None
        self.funding_plan = type('obj', (object,), {'value': 'self_funded'})()
        self.current_stage = type('obj', (object,), {'value': 'Research'})()

# Test the response generation
def test_algorithm():
    from backend.app.api.counselor import detect_question_type, generate_personalized_response
    
    user = MockUser()
    profile = MockProfile()
    
    # Test questions
    test_questions = [
        ("How do I choose the right university?", "university_selection"),
        ("How do I compare different universities?", "university_comparison"),
        ("What are the visa requirements?", "visa_requirements"),
        ("How long does visa processing take?", "visa_timeline"),
        ("What should be my application strategy?", "application_strategy"),
        ("How should I prepare for entrance exams?", "exam_preparation"),
        ("What are my funding options?", "funding_options"),
        ("What are the career outcomes?", "career_outcomes"),
    ]
    
    print(" Testing Counselor Algorithm\n")
    print("=" * 80)
    
    for question, expected_type in test_questions:
        detected_type = detect_question_type(question)
        status = "" if detected_type == expected_type else ""
        print(f"{status} Question: {question}")
        print(f"   Expected: {expected_type}, Got: {detected_type}")
        
        if detected_type == expected_type:
            # Generate response
            response = generate_personalized_response(user, profile, None, expected_type)
            # Check if response is substantial and personalized
            has_user_data = any([
                "$30,000" in response or "$50,000" in response,  # Budget
                "2026" in response,  # Target year
                "3.6" in response or "Strong" in response or "Good" in response,  # GPA
                "Data Science" in response,  # Field of study
                "USA" in response or "Canada" in response or "UK" in response,  # Countries
            ])
            personalized = "" if has_user_data else "️"
            print(f"   {personalized} Response is personalized with user data")
            print(f"    Length: {len(response)} characters")
        print()
    
    print("=" * 80)
    print(" All tests completed!")

if __name__ == "__main__":
    test_algorithm()
