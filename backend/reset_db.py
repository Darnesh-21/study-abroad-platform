"""
Reset database - forcefully drops everything and recreates
"""
from sqlalchemy import text, create_engine
from app.config import get_settings
from app.database import Base
from app.models import User, UserProfile, University, ShortlistedUniversity, TodoItem, ChatMessage

settings = get_settings()
engine = create_engine(settings.database_url)

print(" Forcefully dropping all database objects...")

with engine.begin() as conn:
    # Drop all tables with CASCADE to remove dependencies
    conn.execute(text("DROP TABLE IF EXISTS chat_messages CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS todo_items CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS shortlisted_universities CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS universities CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS user_profiles CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
    
    # Now drop enum types
    conn.execute(text("DROP TYPE IF EXISTS userstage CASCADE"))
    conn.execute(text("DROP TYPE IF EXISTS profilestrength CASCADE"))
    conn.execute(text("DROP TYPE IF EXISTS examstatus CASCADE"))
    conn.execute(text("DROP TYPE IF EXISTS fundingtype CASCADE"))
    conn.execute(text("DROP TYPE IF EXISTS universitycategory CASCADE"))

print(" All objects dropped")

print(" Creating fresh tables...")
Base.metadata.create_all(bind=engine)

print(" Database reset complete! Everything recreated with correct schema.")
