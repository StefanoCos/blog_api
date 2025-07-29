from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.models.models import Post, User
from app.schemas.schemas import PostCreate, PostUpdate, PostResponse, PaginatedResponse
from app.core.security import get_current_active_user
from sqlalchemy import desc

router = APIRouter()

def get_posts_query(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).order_by(desc(Post.created_at)).offset(skip).limit(limit).all()

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_post = Post(**post.dict(), author_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=PaginatedResponse)
def read_posts(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    posts = get_posts_query(db, skip=skip, limit=limit)
    total = db.query(Post).count()
    
    return {
        "total": total,
        "page": (skip // limit) + 1,
        "per_page": limit,
        "items": posts
    }

@router.get("/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    update_data = post_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}
