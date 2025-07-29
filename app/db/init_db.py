from sqlalchemy import create_engine
from app.db.base import Base
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    # Create database URL
    db_url = os.getenv("DATABASE_URL", "sqlite:///./blog.db")
    
    # Create engine
    engine = create_engine(
        db_url, connect_args={"check_same_thread": False} if "sqlite" in db_url else {}
    )
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
