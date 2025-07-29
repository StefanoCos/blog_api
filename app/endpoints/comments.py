from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.models.models import Comment, Post, User
from app.schemas.schemas import CommentCreate, CommentUpdate, CommentResponse, PaginatedResponse
from app.core.security import get_current_active_user
from sqlalchemy import desc

router = APIRouter()

def get_comments_query(db: Session, post_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .order_by(desc(Comment.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = Comment(
        **comment.dict(),
        author_id=current_user.id,
        post_id=post_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/", response_model=PaginatedResponse)
def read_comments(
    post_id: int,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comments = get_comments_query(db, post_id, skip=skip, limit=limit)
    total = db.query(Comment).filter(Comment.post_id == post_id).count()
    
    return {
        "total": total,
        "page": (skip // limit) + 1,
        "per_page": limit,
        "items": comments
    }

@router.get("/{comment_id}", response_model=CommentResponse)
def read_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db)
):
    comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id, Comment.post_id == post_id)
        .first()
    )
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    post_id: int,
    comment_id: int,
    comment_update: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id, Comment.post_id == post_id)
        .first()
    )
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    
    update_data = comment_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(comment, field, value)
    
    db.commit()
    db.refresh(comment)
    return comment

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    post_id: int,
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id, Comment.post_id == post_id)
        .first()
    )
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}
