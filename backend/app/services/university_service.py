import httpx
import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import University

# Free Universities API - No key needed!
UNIVERSITIES_API_BASE = "http://universities.hipolabs.com"

async def fetch_universities_by_country(country: str, limit: int = 100) -> List[dict]:
    """Fetch universities from free Hipolabs API by country"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(
                f"{UNIVERSITIES_API_BASE}/search",
                params={"country": country}
            )
            response.raise_for_status()
            data = response.json()
            # Limit here to avoid huge responses
            return data[:limit] if limit else data
    except Exception as e:
        print(f"Error fetching universities from {country}: {e}")
        return []

async def fetch_universities_by_name(name: str) -> List[dict]:
    """Fetch universities from free Hipolabs API by name"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{UNIVERSITIES_API_BASE}/search",
                params={"name": name}
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"Error fetching universities: {e}")
        return []

def transform_api_data_to_university(api_data: dict, country: str) -> dict:
    """Transform API data to our University model format"""
    
    # Standardize country names to match profile options
    country_mapping = {
        "United States": "USA",
        "United Kingdom": "UK",
        "United States of America": "USA"
    }
    
    # Estimate tuition based on country (rough estimates)
    tuition_estimates = {
        "United States": (30000, 60000),
        "United Kingdom": (20000, 40000),
        "USA": (30000, 60000),
        "UK": (20000, 40000),
        "Canada": (15000, 35000),
        "Australia": (20000, 45000),
        "Germany": (0, 3000),
        "Netherlands": (8000, 20000),
        "France": (2000, 15000),
        "Sweden": (0, 2000),
        "Norway": (0, 1000),
        "India": (2000, 10000),
        "China": (3000, 15000),
        "Japan": (5000, 20000),
        "Singapore": (15000, 35000),
        "South Korea": (5000, 18000),
        "Switzerland": (1000, 8000),
        "New Zealand": (18000, 35000),
        "Ireland": (12000, 25000),
        "Italy": (2000, 12000),
        "Spain": (1500, 10000)
    }
    
    # Get standardized country name
    api_country = api_data.get("country", country)
    standardized_country = country_mapping.get(api_country, api_country)
    
    tuition_min, tuition_max = tuition_estimates.get(country, tuition_estimates.get(standardized_country, (5000, 25000)))
    
    # Estimate acceptance rate (varies by country/type)
    acceptance_rate = 30.0  # Default
    
    # Common fields of study
    common_fields = [
        "Computer Science",
        "Engineering",
        "Business",
        "Medicine",
        "Arts",
        "Sciences",
        "Social Sciences"
    ]
    
    # Common programs
    common_programs = [
        "Bachelor's Degree",
        "Master's Degree",
        "PhD",
        "MBA"
    ]
    
    # Requirements based on country
    requirements = {
        "ielts": 6.5 if standardized_country in ["USA", "UK", "Canada", "Australia"] else 6.0,
        "gre": 300 if standardized_country in ["USA", "Canada"] else 0,
        "gpa": 3.0
    }
    
    return {
        "name": api_data.get("name", "Unknown University"),
        "country": standardized_country,  # Use standardized country name
        "city": None,  # API doesn't provide this
        "ranking": None,  # API doesn't provide this
        "acceptance_rate": acceptance_rate,
        "tuition_fee_min": tuition_min,
        "tuition_fee_max": tuition_max,
        "fields_offered": json.dumps(common_fields),
        "programs": json.dumps(common_programs),
        "requirements": json.dumps(requirements),
        "description": f"University in {country}",
        "website_url": api_data.get("web_pages", [None])[0]
    }

async def import_universities_from_api(db: Session, countries: List[str], limit_per_country: int = 50):
    """Import real universities from API to database"""
    imported_count = 0
    
    # Country name mapping for API calls
    api_country_names = {
        "USA": "United States",
        "UK": "United Kingdom"
    }
    
    for country in countries:
        # Use full country name for API call
        api_country = api_country_names.get(country, country)
        
        print(f"Fetching universities from {api_country}...")
        api_universities = await fetch_universities_by_country(api_country, limit=limit_per_country)
        
        print(f"Received {len(api_universities)} universities from API for {api_country}")
        
        for api_uni in api_universities:
            # Transform first to get standardized country name
            uni_data = transform_api_data_to_university(api_uni, api_country)
            
            # Check if already exists using standardized country
            existing = db.query(University).filter(
                University.name == uni_data["name"],
                University.country == uni_data["country"]
            ).first()
            
            if existing:
                continue
            
            # Create university
            university = University(**uni_data)
            db.add(university)
            imported_count += 1
        
        db.commit()
        print(f"Imported {imported_count} new universities from {api_country}")
    
    return imported_count

async def search_universities_api(country: Optional[str] = None, name: Optional[str] = None) -> List[dict]:
    """Search universities directly from API"""
    if country:
        results = await fetch_universities_by_country(country)
    elif name:
        results = await fetch_universities_by_name(name)
    else:
        return []
    
    return results
