from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment or use the default
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://ab:ijyx5AuWujmQFO8ylDOp55RwBFxIV9pH@dpg-d0ehqgre5dus73fjdk2g-a.oregon-postgres.render.com/snapyz"
)

# Create database engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to provide DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()