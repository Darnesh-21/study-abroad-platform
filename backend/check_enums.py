"""Check what enum values exist in the database"""
from sqlalchemy import text, create_engine
from app.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url)

print(" Checking enum values in Neon database...\n")

with engine.connect() as conn:
    # Check fundingtype enum
    result = conn.execute(text("""
        SELECT e.enumlabel 
        FROM pg_enum e 
        JOIN pg_type t ON e.enumtypid = t.oid 
        WHERE t.typname = 'fundingtype'
        ORDER BY e.enumsortorder
    """))
    
    funding_values = [row[0] for row in result]
    print(f"fundingtype enum has values: {funding_values}")
    print(f"Expected: ['self_funded', 'scholarship_dependent', 'loan_dependent']")
    print(f"Match: {funding_values == ['self_funded', 'scholarship_dependent', 'loan_dependent']}\n")
