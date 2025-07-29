import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import models to ensure they are registered with SQLAlchemy
from app.models.models import Base
from app.db.base import SQLALCHEMY_DATABASE_URL

# Create database tables
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog API",
    description="A simple blog platform with user authentication",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Database URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")

# Include routers
# Import and include routers
try:
    from app.endpoints import users, posts, comments
    
    app.include_router(users.router, prefix="/api/v1", tags=["users"])
    app.include_router(posts.router, prefix="/api/v1/posts", tags=["posts"])
    app.include_router(comments.router, prefix="/api/v1/posts/{post_id}/comments", tags=["comments"])
except Exception as e:
    print(f"Error importing routers: {e}")
    raise

@app.get("/")
async def root():
    return {"message": "Welcome to the Blog API!"}
