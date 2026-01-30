from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Check if we should use SQLite FIRST, before loading settings
use_sqlite = os.getenv("USE_SQLITE", "false").lower() == "true"

if use_sqlite:
    # Use local SQLite for development
    database_url = "sqlite:///./study_abroad.db"
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False}
    )
else:
    # Load settings and use PostgreSQL for production
    settings = get_settings()
    database_url = settings.database_url
    
    # Optimized for Neon (serverless PostgreSQL)
    engine = create_engine(
        database_url,
        pool_pre_ping=True,        # Check connection health
        pool_size=5,                # Connection pool
        max_overflow=10,            # Extra connections if needed
        pool_recycle=3600,          # Recycle connections every hour
        echo=False                  # Set to True for debugging
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
