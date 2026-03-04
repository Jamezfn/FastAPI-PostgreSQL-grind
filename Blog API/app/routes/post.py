from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.db.schemas.posts.post import PostCreate, PostResponse, CursorPostResponse, PostUpdateRequest
from app.utils.protect import get_current_user
from app.db.models.user import User
from app.service.posts.posts import PostService

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create post endpoint"""
    return PostService(session=session).create_post(current_user=current_user, post_data=post_data)

@router.get("/posts/", response_model=CursorPostResponse, status_code=status.HTTP_200_OK)
def get_posts_by_category(category_id: UUID|None=None, cursor: datetime|None=None, limit: int=Query(default=20, gt=0), session: Session = Depends(get_db)):
    """Get post by category endpoint"""
    return PostService(session=session).get_posts_by_category(category_id=category_id,cursor=cursor, limit=limit)

@router.get("/user/posts", response_model=CursorPostResponse, status_code=status.HTTP_200_OK)
def get_posts_by_author(user_id: UUID|None=None, cursor: datetime|None=None, limit: int=Query(default=20, gt=0), session: Session = Depends(get_db)):
    """Get post by user"""
    return PostService(session=session).get_posts_by_author(user_id=user_id, cursor=cursor, limit=limit)

@router.get("/tags/posts", response_model=CursorPostResponse, status_code=status.HTTP_200_OK)
def get_posts_by_tag(tag_name: str, cursor: datetime|None=None, limit: int=Query(default=20, gt=0), session: Session = Depends(get_db)):
    """Get post by tag endpoint"""
    return PostService(session=session).get_post_by_tag(tag_name=tag_name, cursor=cursor, limit=limit)

@router.put("/post/{post_id}", response_model=PostResponse, status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: UUID, post_data: PostUpdateRequest, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> PostResponse:
    """Update post"""
    return PostService(session=session).update_post(post_id=post_id, update_data=post_data, current_user=current_user)